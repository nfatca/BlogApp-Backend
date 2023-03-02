from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers    import PostSerializer, CommentSerializer, LikeSerializer
from .models import Post, Comment, Like , PostView
from rest_framework.exceptions import NotFound
# Create your views here.

class PostMVS(ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer

class CommentMVS(ModelViewSet):
    queryset = Comment.objects.all().select_related('post')
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        if post_id is None:
            return self.queryset()
        else:
            try:
                post = Post.objects.get(id=post_id)
            except Post.DoesNotExist:
                raise NotFound("A post with this is does not exist")
        return self.queryset.filter(post=post)
    
class LikeMVS(ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer