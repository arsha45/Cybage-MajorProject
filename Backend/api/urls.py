from django.urls import path, include
from .views import UserRegistrationAPIView, CustomTokenObtainPairView, AllUsersView,FriendRequestListCreateAPIView, FriendRequestRetrieveUpdateDestroyAPIView,FriendListCreateAPIView, FriendRetrieveUpdateDestroyAPIView, PendingFriendRequestListAPIView,AcceptFriendRequest, FriendListAPIView, RejectFriendRequest, UnfriendAPIView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'allUsers', views.AllUsersView, basename='allUser')

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),

    path('friend-requests/', FriendRequestListCreateAPIView.as_view(), name='friend_request_list_create'),
    path('friend-requests/<int:pk>/', FriendRequestRetrieveUpdateDestroyAPIView.as_view(), name='friend_request_detail'),
    path('friends/', FriendListCreateAPIView.as_view(), name='friend_list_create'),
    path('friends/<int:pk>/', FriendRetrieveUpdateDestroyAPIView.as_view(), name='friend_detail'),
    path('pending-requests/', PendingFriendRequestListAPIView.as_view(), name='pending_friend_requests'),
    path('accept-friend-request/', AcceptFriendRequest.as_view(), name='accept_friend_request'),
    path('friend_list/', FriendListAPIView.as_view(), name='friend_list'),
    path('reject-friend-request/', RejectFriendRequest.as_view(), name='reject_friend_request'),
    path('unfriend/', UnfriendAPIView.as_view(), name='unfriend'),
]
