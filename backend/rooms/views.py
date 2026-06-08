from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Room
from .serializers import RoomSerializer


@api_view(['GET'])
def room_list(request):
    """
    List all rooms or create a new room.
    GET /api/rooms/ - returns all rooms
    """
    rooms = Room.objects.all()
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def room_detail(request, pk):
    """
    Retrieve a single room by ID.
    GET /api/rooms/:id/ - returns one room's details
    """
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response(
            {'error': 'Room not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    serializer = RoomSerializer(room)
    return Response(serializer.data)