from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.db.models import Q 
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from .models import Post, Like, Comment, Follower, FriendRequest, Friend, CustomUser
from .serializers import ReportSerializer, UserRegistrationSerializer, PostSerializer, CommentSerializer, CustomTokenObtainPairSerializer, FollowerSerializer, UserSerializer, UserProfileSerializer, AllUsersSerializer,FriendRequestSerializer, FriendSerializer
User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FollowerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'username'

    @action(detail=True, methods=['POST'], url_path='follow', url_name='follow_user')
    def follow(self, request, pk=None, *args, **kwargs):
        current_user = request.user
        user_to_follow = self.get_object()

        if user_to_follow == current_user:
            return Response({'message': 'You cannot follow yourself!'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            existing_follow = Follower.objects.get(follower=current_user, following=user_to_follow)
        except Follower.DoesNotExist:
            existing_follow = None
        
        if existing_follow:
            existing_follow.delete()
            return Response({'message': 'User unfollowed!'}, status=status.HTTP_200_OK)
        
        Follower.objects.create(follower=current_user, following=user_to_follow)
        return Response({'message': 'User followed!'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['GET'], url_path='followers', url_name='user_followers')
    def user_followers(self, request, *args, **kwargs):
        user = self.get_object()
        followers = [f.following for f in user.following.all()]
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['GET', 'POST','PUT'], url_path='profile', url_name='user_profile')
    def user_profile(self, request, pk=None, *args, **kwargs):
        user = self.get_object()
        if request.method == 'PUT': # PUT method
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else: # GET method
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], url_path='me', url_name='current_user')
    def current_user(self, request, *args, **kwargs):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)    

    @action(detail=True, methods=['GET'], url_path='following', url_name='user_following')
    def user_following(self, request, *args, **kwargs):
        user = self.get_object()
        following = [f.following for f in user.followers.all()]
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'], url_path='posts', url_name='user_posts')
    def user_posts(self, request, *args, **kwargs):
        user = self.get_object()
        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'], url_path='feed', url_name='user_feed')
    def user_feed(self, request, *args, **kwargs):
        user = self.get_object()
        following = [f.following for f in user.following.all()]
        posts = Post.objects.filter(Q(user=user) | Q(user__in=following))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['GET'], url_path='liked', url_name='user_liked_posts')
    def user_liked_posts(self, request, *args, **kwargs):
        user = self.get_object()
        posts = Post.objects.filter(like__user=user)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserRegistrationAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        reponse = super().create(request, *args, **kwargs)
        user = User.objects.get(email=request.data['email'])

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        reponse.data['access_token'] = access_token

        return reponse


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, media=self.request.data.get('media'))

    # Post Actions
    @action(detail=True, methods=['PUT'], url_path='edit', url_name='edit_post')
    def edit_post(self, request, pk=None):
        try:
            post = self.get_object()
            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['DELETE'], url_path='delete', url_name='delete_post')
    def delete_post(self, request, pk=None):
        try:
            post = self.get_object()
            post.delete()
            return Response({'message': 'Post deleted!'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['POST'], url_path='like', url_name='like_post')
    def like_post(self, request, pk=None):
        try:
            post = self.get_object()
            like, created = Like.objects.get_or_create(
                user=request.user, post=post)
            if created:
                post.likes_count += 1
                post.save()
                return Response({'message': 'Post liked!'}, status=status.HTTP_201_CREATED)
            else:
                post.likes_count = max(0, post.likes_count - 1)
                post.save()
                like.delete()
                return Response({'message': 'Post unliked!'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'message': 'Post does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    # Comment Actions
    @action(detail=True, methods=['GET'], url_path='comments', url_name='post_comments')
    def post_comments(self, request, pk=None):
        post = self.get_object()
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], url_path='comment', url_name='comment_post')
    def comment_post(self, request, pk=None):
        post = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllUsersView(viewsets.ReadOnlyModelViewSet):
    serializer_class = AllUsersSerializer

    def get_queryset(self):
        # Retrieve the logged-in user
        logged_in_user = self.request.user

        # Get all users except the logged-in user and superuser
        queryset = CustomUser.objects.exclude(id=logged_in_user.id).exclude(is_superuser=True)

        # Filter out users who are friends of the logged-in user
        friends = logged_in_user.friends.all()
        queryset = queryset.exclude(id__in=[friend.friend.id for friend in friends])

        return queryset

class FriendRequestListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        # Filter friend requests based on the current user and pending status
        current_user = self.request.user
        return FriendRequest.objects.filter(to_user=current_user, status='pending')

    def create(self, request, *args, **kwargs):
        from_user_id = request.data.get('from_user_id')
        to_user_id = request.user.id

        # Check if a friend request already exists between the sender and the recipient
        existing_request = FriendRequest.objects.filter(from_user_id=from_user_id, to_user_id=to_user_id).exists()
        if existing_request:
            return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating the friend request if it doesn't already exist
        return super().create(request, *args, **kwargs)

class FriendRequestRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer

class FriendListCreateAPIView(generics.ListCreateAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

class FriendRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer

class PendingFriendRequestListAPIView(ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        current_user = self.request.user
        return FriendRequest.objects.filter(to_user=current_user, status='pending')

class FriendListAPIView(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Retrieve all friends of the logged-in user
        return Friend.objects.filter(user=user)

class AcceptFriendRequest(APIView):
    def post(self, request):
        from_user_id = request.data.get('from_user_id')
        current_user = request.user

        # Retrieve the pending friend request with the specified criteria
        friend_requests = FriendRequest.objects.filter(
            from_user_id=from_user_id, 
            to_user=current_user, 
            status='pending'
        )

        if not friend_requests.exists():
            return Response({'error': 'Friend request does not exist or has already been accepted'}, status=status.HTTP_404_NOT_FOUND)

        if friend_requests.count() > 1:
            return Response({'error': 'Multiple pending friend requests found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Only one friend request found
        friend_request = friend_requests.first()

        # Check if the users are already friends
        if Friend.objects.filter(user=current_user, friend=friend_request.from_user).exists():
            return Response({'error': 'Users are already friends'}, status=status.HTTP_400_BAD_REQUEST)

        # Create friend relationships for both users
        try:
            with transaction.atomic():
                # For the user accepting the request
                friend_instance = Friend.objects.create(user=current_user, friend=friend_request.from_user)
                
                # For the user who sent the request
                reverse_friend_instance = Friend.objects.create(user=friend_request.from_user, friend=current_user)

                # Update friend request status and accept the request
                friend_request.status = 'accepted'
                friend_request.save()

                # Optionally, you can update the friend lists of the users here if needed

        except IntegrityError:
            return Response({'error': 'Failed to create friend relationship'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Serialize the friend data and return response
        serializer = FriendSerializer(friend_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RejectFriendRequest(APIView):
    def post(self, request):
        from_user_id = request.data.get('from_user_id')
        current_user = request.user

        # Retrieve the pending friend request with the specified criteria
        friend_requests = FriendRequest.objects.filter(
            from_user_id=from_user_id, 
            to_user=current_user, 
            status='pending'
        )

        if not friend_requests.exists():
            return Response({'error': 'Friend request does not exist or has already been rejected'}, status=status.HTTP_404_NOT_FOUND)

        if friend_requests.count() > 1:
            return Response({'error': 'Multiple pending friend requests found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Only one friend request found
        friend_request = friend_requests.first()

        # Update friend request status to 'rejected'
        friend_request.status = 'rejected'
        friend_request.save()

        return Response({'message': 'Friend request rejected successfully'}, status=status.HTTP_200_OK)

class UnfriendAPIView(APIView):
    def post(self, request):
        friend_username = request.data.get('friend_username')
        current_user = request.user

        try:
            # Retrieve the friend's user object
            friend_user = User.objects.get(username=friend_username)
        except User.DoesNotExist:
            raise ValidationError("Friend with the provided username does not exist")

        # Check if there is a friend relationship between the current user and the friend
        try:
            friend_relationship = Friend.objects.get(user=current_user, friend=friend_user)
        except Friend.DoesNotExist:
            raise ValidationError("You are not friends with the specified user")

        # Delete the friend relationship
        friend_relationship.delete()

        # Also delete any related friend requests
        FriendRequest.objects.filter(
            Q(from_user=current_user, to_user=friend_user) | Q(from_user=friend_user, to_user=current_user)
        ).delete()

        return Response({'message': 'Friend unfriended successfully'}, status=status.HTTP_200_OK)


class ReportPostView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        content = request.data.get('content')
        reason = request.data.get('reason')
        postUser = request.data.get('postUser')
         

        # Validate input data
        if not all([username, content, reason, postUser]):
            return Response({'error': 'Incomplete data provided'}, status=status.HTTP_400_BAD_REQUEST)

        # Save reported post
        report_data = {'username': username, 'content': content, 'reason': reason, 'postUser':postUser }
        serializer = ReportSerializer(data=report_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)