from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from .serializer import PostSerializer, CommentSerializer
from .models import Post, Comment, Like
from CommunityApp.models import Section, Club
from BasicApp.models import Course
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response({'post': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def post_detail(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=id)

        serializer = PostSerializer(post)
        return Response({'post': serializer.data}, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        post = get_object_or_404(Post, id=id)

        if post.author == request.user:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        post = get_object_or_404(Post, id=id)

        if  post.author == request.user:
            post.delete()
            return Response("deleted successfully", status=status.HTTP_200_OK)
        else:
            return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    return Response({'error': "Not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def section_posts(request, id):
    section = get_object_or_404(Section, id=id)
    if section != request.user.section:
        return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    posts = Post.objects.filter(section=section)
    serialize = PostSerializer(posts, many=True)
    return Response({'posts': serialize.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def club_posts(request, id):
    club = get_object_or_404(Club, id=id)
    posts = Post.objects.filter(club=club)
    serialize = PostSerializer(posts, many=True)

    return Response({'posts': serialize.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_posts(request, id):
    course = get_object_or_404(Course, id=id)
    posts = Post.objects.filter(course=course)
    serialize = PostSerializer(posts, many=True)

    return Response({'posts': serialize.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def general_posts(request):
    posts = Post.objects.filter(Q(section=None) and Q(club=None))
    serialize = PostSerializer(posts, many=True)

    return Response({'posts': serialize.data}, status=status.HTTP_200_OK)


### comment GET, POST, DELETE and PUT

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def get_or_create_comment(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=id)
        comments = Comment.objects.filter(post=post)
        if comments:
            serializer = CommentSerializer(comments, many=True)
            return Response({'comment': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': "Not found"}, status=status.HTTP_404_NOT_FOUND)
    elif request.method == 'POST':
        post = get_object_or_404(Post, id=id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, post=post)
            return Response({'comment': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_or_delete_comment(request, id):
    if request.method == 'DELETE':
        comment = get_object_or_404(Comment, id=id)

        if comment.user == request.user:
            comment.delete()
            return Response("deleted successfully", status=status.HTTP_200_OK)
        return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'PUT':
        comment = get_object_or_404(Comment, id=id)

        if comment.user == request.user:
            serializer = PostSerializer(comment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    return Response({'error': "Not found"}, status=status.HTTP_404_NOT_FOUND)

### like GET, POST, DELETE and PUT

@api_view(['GET'])
def get_likes_count(request, id):
    post = get_object_or_404(Post, id=id)
    like_count = Like.objects.filter(post=post).count()

    return Response({"like count": like_count}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike(request, id):
    get_object_or_404(Like, id=id).delete()
    return Response("unliked", status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like(request, id):
    post = get_object_or_404(Post, id=id)
    Like.objects.create(user=request.user, post=post).save()
    return Response("liked", status=status.HTTP_200_OK)


