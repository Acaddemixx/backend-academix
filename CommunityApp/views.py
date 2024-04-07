from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializer import *
from .models import *
from django.shortcuts import get_object_or_404
from pgvector.django import L2Distance
from AI.main import embed

#++++++++++++++++++++ POST METHODS +++++++++++++++++++++++++++

#----------------- create club -------------------------------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_club(request):
    request_data = request.data
    serializer = ClubSerializer(data= request_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#=============================================================================

#------------------------- create section -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_section(request):
    request_data = request.data
    serializer = SectionSerializer(data= request_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#=============================================================================

#----------------------- create event ------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    request_data = request.data
    serializer = EventSerializer(data= request_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#=============================================================================


#+++++++++++++++++++++++ GET METHODS ++++++++++++++++++++++++++++

#---------------- get club -------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_club(request):
    club = get_object_or_404(Club , name = request.data['name'])
    serializer = ClubSerializer(instance=club)

    return Response(serializer.data , status=status.HTTP_200_OK)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_clubs(request):
    clubs = Club.objects.all()
    serializer = ClubSerializer(instance= clubs , many = True)

    return Response({'clubs': serializer.data} , status=status.HTTP_200_OK)

        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_related_club(request):
    club_name = request.data['name']
    search_embedding = embed(club_name)
    clubs = Club.objects.order_by(L2Distance('embedding' , search_embedding))

    serializer = ClubSerializer(instance=clubs , many = True)

    return Response(serializer.data , status= status.HTTP_200_OK)
  

#===================================================================


#----------------------- get section -----------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_section(request):
    section = get_object_or_404(Section , name = request.data['name'])
    serializer = ClubSerializer(instance=section)

    return Response(serializer.data , status=status.HTTP_200_OK)


#=========================================================


#-----------------------get event------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event(request):
    event = get_object_or_404(Event , name = request.data['name'])
    serializer = ClubSerializer(instance=event)

    if serializer.is_valid():
        return Response(serializer.data , status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors , status = status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(instance=events , many = True)

    return Response({'events':serializer.data} , status=status.HTTP_404_NOT_FOUND)
 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_related_events(request):
    request_embedding = embed(request.data['name'])
    events = Event.objects.order_by(L2Distance('embedding' , request_embedding))
    serializer = EventSerializer(instance=events , many = True)

    return Response({'events':serializer.data} , status=status.HTTP_200_OK)

#=========================================================================

#+++++++++++++++++++++++++ UPDATE METHODES ++++++++++++++++++++++++++++++


#------------------- update club ----------------------------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_club(request, pd):
    club = get_object_or_404(Club , id = pd)
    serializer = ClubSerializer(instance=club)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)
    else:
        return Response(serializer.errors)
    
#=========================================================================

#------------------------- update section ---------------------------------


