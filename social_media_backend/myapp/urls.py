# myapp/urls.py
from django.urls import path
from .views import SignUpView, PostList, UserPostList # make sure to import PostList if you are using it
from rest_framework.authtoken.views import obtain_auth_token
from .views import friend_suggestions, my_user_view
from .views import send_friend_request, approve_friend_request,get_conversations
from .views import friend_requests_list, friends_list
from .views import profile_view,user_posts, own_profile_view, own_posts, get_messages, send_message
 
urlpatterns = [
    path('api/posts/', PostList.as_view(), name='post-list'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', obtain_auth_token, name='api_token_auth'),
    path('api/user/posts', UserPostList.as_view(), name='user-post-list'),
    path('api/friend-suggestions/', friend_suggestions, name='friend-suggestions'),
    path('send-friend-request/<str:username>/', send_friend_request, name='send-friend-request'),
    path('approve-friend-request/<int:request_id>/', approve_friend_request, name='approve-friend-request'),
    path('api/friend-requests/', friend_requests_list, name='friend-requests-list'),
    path('api/friends-list/', friends_list, name='friends-list'),
    path('api/profile/<str:username>/', profile_view, name='profile-view'),
    path('api/user/<str:username>/posts', user_posts, name='user-posts'),
    path('api/ownprofile/', own_profile_view, name='own-profile-view'),
    path('api/ownposts/', own_posts, name='own-posts'),
    path('api/messages/<str:username>/', get_messages, name='get-messages'),
    path('api/messages/', send_message, name='send-message'),
    path('api/myuser/', my_user_view, name='my-user'),
    path('api/get_conversations/', get_conversations, name='get_conversations'),
    # ... other paths for your app
]



