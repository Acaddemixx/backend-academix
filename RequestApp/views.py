from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .serializer import RequestSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Request
from CommunityApp.views import create_club_from_request , create_event_from_request
from PostApp.views import create_post_from_request


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_request(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(student=request.user)
        return Response({'request': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated , IsAdminUser])
#for admin to get all the requests
def get_all_requests(request):
    requests = Request.objects.all()
    serializer = RequestSerializer(requests, many=True)
    return Response({'requests': serializer.data}, status=status.HTTP_200_OK)



#user deleting the request
@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delete_request(request,id):
    req = get_object_or_404(Request, id=id)
    if request.data.get('status') == "Accepted":
        if req.post:
            create_post_from_request(req)
        elif req.club:
            create_club_from_request(req.club)
        elif req.event:
            create_event_from_request(req)
    elif request.data.get('status') == "Decline":
        req.delete()
    
    return Response("successful", status=status.HTTP_200_OK)

################################################################################

#Report views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_report(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'report': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
#for admins to get all reports
def get_pending_report(request):
    if request.user.is_admin :
        requests = Request.objects.filter(status = 3)
        serializer = RequestSerializer(requests, many=True)
        return Response({'reports': serializer.data}, status=status.HTTP_200_OK)
    return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

#for user to get all his reports
def get_all_report(request,id):
    reports = get_object_or_404(Request, id=id)
    serializer = RequestSerializer(reports, many=True)
    return Response({'reports': serializer.data}, status=status.HTTP_200_OK)

#user deleting the reports
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_report(request,id):
    rep = get_object_or_404(Request, id=id)
    if rep.user == request.user:
        rep.delete()
        return Response("Deleted successfully", status=status.HTTP_200_OK)
    return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
