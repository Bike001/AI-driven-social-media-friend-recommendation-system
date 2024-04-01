from django.contrib import admin
from .models import Post
from .models import Friendship, FriendRequest, Message


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'published_date', 'sentiment')

admin.site.register(Post, PostAdmin)

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2')

@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'to_user', 'accepted']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'timestamp')
    # Other configurations if needed