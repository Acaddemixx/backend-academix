from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
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
    serializer = ClubSerializer(instance=club , data= request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)
    else:
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    
#=========================================================================

#------------------------- update section ---------------------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_section(request, pd):
    section = get_object_or_404(Section , id = pd)
    serializer = SectionSerializer(instance=section , data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)
    else:
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

#=========================================================================

#----------------------------- update event ------------------------------

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, pd):
    event = get_object_or_404(Event , id = pd)
    serializer = EventSerializer(instance=event , data = request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data , status= status.HTTP_200_OK)
    else:
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)

#=========================================================================

#++++++++++++++++++++++++ DELETE METHODES +++++++++++++++++++++++++++++++

#------------------------- delete club -----------------------------------

@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delete_club(request , pk):
    club = get_object_or_404(Club , id = pk)
    serializer = ClubSerializer(instance=club)
    serialized_data = serializer.data 
    club.delete()
    return Response({'deleted_club': serialized_data} , status=status.HTTP_202_ACCEPTED)

#===========================================================================

#------------------------- delete section ----------------------------------

@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delete_section(request , pk):
    section = get_object_or_404(Section, id = pk)
    serializer = SectionSerializer(instance=section)
    serialized_data = serializer.data 
    section.delete()
    return Response({'deleted_section': serialized_data} , status=status.HTTP_202_ACCEPTED)

#============================================================================

#-------------------------- delete event ------------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated , IsAdminUser])
def delete_event(request , pk):
    event = get_object_or_404(Event, id = pk)
    serializer = EventSerializer(instance=event)
    serialized_data = serializer.data 
    event.delete()
    return Response({'deleted_event': serialized_data} , status=status.HTTP_202_ACCEPTED)

#============================================================================