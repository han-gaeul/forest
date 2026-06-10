from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


@api_view(['GET', 'POST'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.prefetch_related('comments').all()
        return Response(PostSerializer(posts, many=True).data)

    content = request.data.get('content', '').strip()
    if not content:
        return Response({'error': '내용을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    post = Post.objects.create(content=content)
    return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def post_like(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': '없는 글입니다.'}, status=status.HTTP_404_NOT_FOUND)
    post.likes += 1
    post.save(update_fields=['likes'])
    return Response({'likes': post.likes})


@api_view(['POST'])
def comment_create(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return Response({'error': '없는 글입니다.'}, status=status.HTTP_404_NOT_FOUND)
    content = request.data.get('content', '').strip()
    if not content:
        return Response({'error': '내용을 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)
    comment = Comment.objects.create(post=post, content=content)
    return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
