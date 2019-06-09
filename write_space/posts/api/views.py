from rest_framework.generics import (ListAPIView,RetrieveAPIView
,RetrieveUpdateAPIView,RetrieveDestroyAPIView,CreateAPIView)

from rest_framework.permissions import (AllowAny,IsAuthenticated,IsAdminUser
,IsAuthenticatedOrReadOnly)
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from posts.api.permissions import IsOwnerOrReadOnly

from posts.models import Post,Comment
from posts.api import serializers

from .pagination import postLimitOffsetPagination,postPageNumberPagination

class postListApiView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.postListSerializer
    permission_classes = [AllowAny]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ["title","text","author__username","publish_date","post_heading"]
    pagination_class = postPageNumberPagination#postLimitOffsetPagination


class postDetailApiView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.postDetailSerializer
    permission_classes = [AllowAny]

class postUpdateApiView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.postDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]

    def perform_update(self,serializer):
        serializer.save(author=self.request.user)

class postDeleteApiView(RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.postDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]


class postCreateApiView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.postCreateSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def perform_create(self,serializer):
        serializer.save(author=self.request.user)

class commentsApiView(ListAPIView):
    serializer_class = serializers.postCommentsSerializer
    permission_classes = [AllowAny]

    def get_queryset(self,*args,**kwargs):
        return Comment.objects.filter(post__pk=self.kwargs.get("pk"))

class addCommentApiView(CreateAPIView):
    serializer_class = serializers.addCommentSerializer

    def perform_create(self,serializer,*args,**kwargs):
        serializer.save(author=self.request.user,post=Post.objects.get(pk=self.kwargs.get("pk")))

class editCommentApiView(DestroyModelMixin,UpdateModelMixin,RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.editCommentSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)

    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)
