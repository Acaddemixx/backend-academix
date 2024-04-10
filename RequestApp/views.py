from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import RequestSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Request

#Request views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_request(request):
    serializer = RequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(student=request.user.student)
        return Response({'request': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_request(request,id):
    original_request = get_object_or_404(Request, id=id)
    if request.user.is_admin and original_request.status == 3:
        serializer = RequestSerializer(request, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif original_request.student == request.user:
        serializer = RequestSerializer(request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
#for a specific user to get accepted request
def get_accepted_requests(request,id):
    req = get_object_or_404(Request, id=id)
    req = req.filter(status= 1)
    serialize = RequestSerializer(req, many=True)
    return Response({'requests': serialize.data}, status=status.HTTP_200_OK)
 
#for a specific user to get denied request
def get_denied_requests(id):
    req = get_object_or_404(Request, id=id)
    req = req.filter(status= 2)
    serialize = RequestSerializer(req, many=True)
    return Response({'requests': serialize.data}, status=status.HTTP_200_OK)

#for a specific user to get pending request
def get_denied_requests(id):
    req = get_object_or_404(Request, id=id)
    req = req.filter(status= 3)
    serialize = RequestSerializer(req, many=True)
    return Response({'requests': serialize.data}, status=status.HTTP_200_OK)

#for admin to get all the requests
def get_pending_requests(request):
    if request.user.is_admin :
        requests = Request.objects.filter(status = 3)
        serializer = RequestSerializer(requests, many=True)
        return Response({'requests': serializer.data}, status=status.HTTP_200_OK)
    return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)



#user deleting the request
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_request(request,id):
    req = get_object_or_404(Request, id=id)
    if req.student == request.user:
        req.delete()
        return Response("Deleted successfully", status=status.HTTP_200_OK)
    return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

#Report views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_report(request):
    serializer = RequestSerializer(data=request.data)
    if request.data.get('club') != None:
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({'report': serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_report(request,id):
    original_request = get_object_or_404(Request, id=id)
    if request.user.is_admin and original_request.status == 3:
        serializer = RequestSerializer(request, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif original_request.student == request.user:
        serializer = RequestSerializer(request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)


#for admins to get all reports
def get_pending_report(request):
    if request.user.is_admin :
        requests = Request.objects.filter(status = 3)
        serializer = RequestSerializer(requests, many=True)
        return Response({'reports': serializer.data}, status=status.HTTP_200_OK)
    return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)

#for user to get all his reports
def get_pending_requests(request,id):
    reports = get_object_or_404(Request, id=id)
    serializer = RequestSerializer(reports, many=True)
    return Response({'reports': serializer.data}, status=status.HTTP_200_OK)

#user deleting the reports
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_request(request,id):
    req = get_object_or_404(Request, id=id)
    if req.user == request.user:
        req.delete()
        return Response("Deleted successfully", status=status.HTTP_200_OK)
    return Response({'error': "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
