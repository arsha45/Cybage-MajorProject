from django.contrib import admin
from .models import CustomUser, Follower, Like, Post, Comment

# Register your models here.
class UserAdminView(admin.ModelAdmin):
    list_display = [ 'email', 'date_joined']
admin.site.register(CustomUser, UserAdminView)

class PostAdminView(admin.ModelAdmin):
    list_display = ['user', 'title', 'content']
admin.site.register(Post, PostAdminView)

class CommentAdminView(admin.ModelAdmin):
    list_display = ['user', 'post', 'content']
admin.site.register(Comment, CommentAdminView)

class LikeAdminView(admin.ModelAdmin):
    list_display = ['user', 'post', 'date_liked']
admin.site.register(Like, LikeAdminView)

class FollowerAdminView(admin.ModelAdmin):
    list_display = ['follower', 'following', 'date_followed']
admin.site.register(Follower, FollowerAdminView)