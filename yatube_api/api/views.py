from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from posts.models import Post, Group, Comment


class PostListViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostListViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        post = get_object_or_404(Post, id=instance.id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentListViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        #  post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        #  queryset = Comment.objects.filter(post=post_id)
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user,
                        post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentListViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        comment = get_object_or_404(Comment, id=instance.id)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
