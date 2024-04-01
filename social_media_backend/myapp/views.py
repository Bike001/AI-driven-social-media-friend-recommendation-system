# myapp/views.py
# Standard library imports
from collections import defaultdict
import logging

# Django imports
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Q, Subquery, OuterRef
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Django Rest Framework imports
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

# Local application imports
from .models import FriendRequest, Friendship, Message, Post, User
from .serializers import FriendRequestSerializer, MessageSerializer, PostSerializer, UserSerializer

# External library imports
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Local module (assuming it's a custom module in the same Django app)
from .emotion_logic import get_similar_emotions


# views.py (at the top)
model_name = "SamLowe/roberta-base-go_emotions"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
model.eval()  # Set the model to evaluation mode

# @login_required
logger = logging.getLogger(__name__)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_suggestions(request):
    # Get the latest post by the user
    latest_post = Post.objects.filter(user=request.user).order_by('-published_date').first()
    latest_emotion = latest_post.sentiment if latest_post else 'neutral'  # fallback to 'neutral' if no posts
    recommended_users = recommend_friends(request.user, latest_emotion)
    logger.debug("Recommended Users: %s", recommended_users)

    # Exclude users who are already friends
    friends = get_friends_of_user(request.user)
    friends_usernames = [friend.username for friend in friends]
    recommended_users = [user for user in recommended_users if user['username'] not in friends_usernames]

    return Response(recommended_users)



def recommend_friends(user_posting, emotion):
    similar_emotions = get_similar_emotions(emotion)
    print("Similar Emotions:", similar_emotions)  # Debug print statement
    recommended_users_qs = User.objects.filter(
        post__sentiment__in=similar_emotions
    ).exclude(
        id=user_posting.id
    ).distinct()[:10]

    # Debug print statements
    print("QuerySet:", recommended_users_qs)
    recommended_users = UserSerializer(recommended_users_qs, many=True).data
    print("Recommended Users Data:", recommended_users)
    return recommended_users

    # If you want to return serialized data
    # from within this function, you would serialize
    # the queryset here and return the serialized data.
    recommended_users = UserSerializer(recommended_users_qs, many=True).data
    return recommended_users

@method_decorator(csrf_exempt, name='dispatch')

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-published_date')
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user if self.request.user.is_authenticated else None)
        
        # Run sentiment analysis
        with torch.no_grad():
            inputs = tokenizer(post.content, return_tensors="pt", padding=True, truncation=True, max_length=512)
            outputs = model(**inputs)
            probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
            predicted_emotion_idx = probabilities.argmax().item()
            emotion_labels = [
               "admiration", "amusement", "anger", "annoyance", "approval", "caring", "confusion", "curiosity",
                "desire", "disappointment", "disapproval", "disgust", "embarrassment", "excitement", "fear", "gratitude",
                "grief", "joy", "love", "nervousness", "optimism", "pride", "realization", "relief", "remorse", "sadness", "surprise", "neutral"
            ]
            predicted_emotion = emotion_labels[predicted_emotion_idx]
            post.sentiment = predicted_emotion
            post.save()

        # Get recommended friends based on sentiment
        if post.sentiment:
            recommended_users = recommend_friends(post.user, post.sentiment)
            
            # Here we are just returning the recommended friends in the response.
            # If you want to associate them with the post, you can save them in a ManyToManyField.
            # e.g., post.recommended_friends.set([user.id for user in recommended_users_qs])

            # Complete the post creation response with friend recommendations
            headers = self.get_success_headers(serializer.data)
            return Response({
                'post': serializer.data, 
                'recommended_friends': recommended_users
            }, status=status.HTTP_201_CREATED, headers=headers)
        


from rest_framework.permissions import AllowAny

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  # This allows access without authentication

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # You might want to create a token for the user here as well
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class UserPostList(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # This will only return posts for the currently logged-in user
        return Post.objects.filter(user=self.request.user)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request, username):
    try:
        to_user = User.objects.get(username=username)
        if to_user == request.user:
            return Response({"error": "Cannot send friend request to yourself."}, status=status.HTTP_400_BAD_REQUEST)
        FriendRequest.objects.get_or_create(from_user=request.user, to_user=to_user)
        return Response(status=status.HTTP_201_CREATED)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def approve_friend_request(request, request_id):
    try:
        friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user, accepted=False)
        friend_request.accepted = True
        friend_request.save()

        # Sort the users by ID to avoid comparison issues and to maintain the integrity of the unique constraint
        user1, user2 = sorted([friend_request.from_user, friend_request.to_user], key=lambda u: u.id)
        Friendship.objects.get_or_create(user1=user1, user2=user2)

        # This is to update the frontend with the accepted friend request and the new friend added
        friend_request_serializer = FriendRequestSerializer(friend_request)
        new_friend_serializer = UserSerializer(user2)
        return Response({
            'friend_request': friend_request_serializer.data,
            'new_friend': new_friend_serializer.data
        }, status=status.HTTP_200_OK)

    except FriendRequest.DoesNotExist:
        return Response({"error": "Friend request does not exist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"An error occurred while approving friend request: {e}")
        return Response({"error": "An internal server error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_requests_list(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, accepted=False)
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data)


def get_friends_of_user(user):
    # This function should return a combined queryset of all friends
    friends_received = User.objects.filter(
        friend_requests_received__from_user=user, 
        friend_requests_received__accepted=True
    )
    friends_sent = User.objects.filter(
        friend_requests_sent__to_user=user, 
        friend_requests_sent__accepted=True
    )
    return friends_received.union(friends_sent)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friends_list(request):
    # Fetch the friends of the current user
    user = request.user
    friends = User.objects.filter(
         Q(friendships1__user2=request.user) | 
         Q(friendships2__user1=request.user)
    ).distinct()
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def profile_view(request, username):
    # Retrieve the user by username
    user = get_object_or_404(User, username=username)
    
    # If you have a user profile model, fetch it and serialize it
    # Otherwise, serialize the user instance directly
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by('-published_date')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def own_profile_view(request):
    # Use the user from the request to retrieve their profile data
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def own_posts(request):
    # Fetch posts for the logged-in user
    posts = Post.objects.filter(user=request.user).order_by('-published_date')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_messages(request, username):
    user = request.user
    friend = User.objects.get(username=username)
    messages = Message.objects.filter(sender=friend, receiver=user) | Message.objects.filter(sender=user, receiver=friend)
    messages = messages.order_by('timestamp')
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_message(request):
    receiver_username = request.data.get('receiver_username')
    content = request.data.get('content')
    if not receiver_username or not content:
        return Response({"error": "Missing receiver username or content"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return Response({"error": "Receiver username not found"}, status=status.HTTP_404_NOT_FOUND)

    message = Message.objects.create(
        sender=request.user,
        receiver=receiver,
        content=content
    )
    return Response(status=status.HTTP_201_CREATED)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_user_view(request):
    # The request.user will contain the user object of the currently authenticated user
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversations(request):
    # Get all messages where the user is the sender or receiver
    messages = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-timestamp')  # Order by timestamp to get latest messages

    # Group messages by conversation partner
    conversations = defaultdict(list)
    for message in messages:
        partner = message.receiver if message.sender == request.user else message.sender
        conversations[partner.username].append(MessageSerializer(message).data)
    
    # Prepare the response data
    conversations_data = [
        {'username': username, 'messages': msgs}
        for username, msgs in conversations.items()
    ]
    
    # Log the data to the console for debugging
    print(conversations_data)

    return Response(conversations_data)

