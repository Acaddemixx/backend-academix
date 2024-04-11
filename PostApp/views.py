from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from .serializer import PostSerializer, CommentSerializer
from .models import Post, Comment, Like
from CommunityApp.models import Section, Club 
from RequestApp.models import Notification , Request
from BasicApp.models import Course
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from AI import general, main
from PIL import Image
from UserApp.serializer import MyUserSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    gemini = general.LLM()
    content_validation = gemini.verify_test_content(request.data['content'])
    img_validation = True

    if main.is_image(request.data['file']):
        img_validation = gemini.verify_image_content(request.data['file'])
    
        
    if not img_validation:
        report = "This content can not be posted, because: " + gemini.image_report(request.data['file'])
        return Response({'report': report}, status=status.HTTP_400_BAD_REQUEST)

    if not content_validation:
        report = "This content can not be posted"
        return Response({'report': report}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response({'post': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated , IsAdminUser])
def create_post_from_request(request):
    post = request.data['post']
    serializer = PostSerializer(data= post)

    notify = Notification(to_user = request.data['student'] , status = 2 , content = "Request Aproved")
    notify.save()

    request_obj = Request.objects.get(id = request.data['id'])
    request_obj.delete()
    
    if serializer.is_valid():
        serializer.save(author = request.data['student'])
        return Response({'post': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def post_detail(request, id):
    if request.method == 'GET':
        post = get_object_or_404(Post, id=id)

        serializer = PostSerializer(post).data

        serializer['author'] = MyUserSerializer(instance = post.author)

        return Response({'post': serializer}, status=status.HTTP_200_OK)
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
    posts = Post.objects.filter(section=None , club=None)
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_requested_post(request):
    post_object = request.data['post']
    serializer = PostSerializer(data= post_object)
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response({'post': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

