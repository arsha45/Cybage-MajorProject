from django.contrib import admin
from .models import CustomUser, Follower, Like, Post, Comment,FriendRequest, Friend, ReportedPost

# Register your models here.
class UserAdminView(admin.ModelAdmin):
    list_display = [ 'username','email','is_active']

    search_fields = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),  
        ('Personal Info', {'fields': ('bio', 'profile_picture', 'birthdate')}),  
        ('Permissions', {'fields': ('is_active',)})
    )

    actions = ['activate_users', 'deactivate_users']  

    def activate_users(self, request, queryset):
        queryset.update(is_active=True)
    activate_users.short_description = "Activate selected users"

    def deactivate_users(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_users.short_description = "Deactivate selected users"

    def get_queryset(self, request):
        # Retrieve queryset excluding superusers
        queryset = super().get_queryset(request)
        return queryset.exclude(is_superuser=True)


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

class FriendRequestAdminView(admin.ModelAdmin):
        list_display = ['from_user', 'to_user', 'status']
admin.site.register(FriendRequest, FriendRequestAdminView)

class FriendAdminView(admin.ModelAdmin):
        list_display = ['user', 'friend']
admin.site.register(Friend, FriendAdminView)


class ReportAdminView(admin.ModelAdmin):
    list_display = ['username','postUser','content','reason']
admin.site.register(ReportedPost, ReportAdminView)


admin.site.site_header = "Social Media"  
admin.site.site_title = "Admin Pannel"   
admin.site.index_title = "Social Media" 