from extuser.models import MyUser as User
from rest_framework import filters
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from models import Post
from serializer import UserSerializer, PostSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    /api/v1/user/ [GET]- list of all users. Required permissions.
    /api/v1/user/<id> [GET]- get info about user id = id. Required permissions.
    /api/v1/user/<id> [DELETE]- delete user with id= id. Required permissions.
    /api/v1/user/<id> [PUT]- update user with id= id. Required permissions.
    /api/v1/user/ [POST]- create user. Required permissions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser,)


class PostViewSet(viewsets.ModelViewSet):
    """
    /api/v1/user/ [GET]- list of all posts.
    /api/v1/user/<id> [GET]- get info about post by id.
    /api/v1/user/<id> [DELETE]- delete post with id= id.
    /api/v1/user/<id> [PUT]- update post with id= id.
    /api/v1/user/ [POST]- create post.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('title','author')


class UserPostList(generics.ListAPIView):
    """
    /api/v1/<userId>/post/ [GET]-Return list of all posts by userId.
    """
    model = Post
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        userId = self.kwargs['userId']
        return Post.objects.filter(author__id=userId)


class UserRegister(generics.CreateAPIView):
    """
    /api/v1/register/ [POST]-Register new user
    """
    model = User
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserProfile(generics.ListAPIView):
    """
    /api/v1/profile/ [GET]-Return users profile
    """
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(email=user)




