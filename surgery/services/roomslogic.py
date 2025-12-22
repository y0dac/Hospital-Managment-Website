from ..models import Room , RoomDevice ,Surgery
from django.utils import timezone

def availablerooms():
    rooms = Room.objects.filter(
        is_available = True 
    )
    returnedrooms = []
    for room in rooms :
        returnedrooms.append({"Room" : room.id , "device" : RoomDevice.objects.filter(room = room)})

    return returnedrooms    

def autofree():
    today = timezone.now().date()

    surgeries = Surgery.objects.filter(date__lt=today)

    for surgery in surgeries:
        room = surgery.room
        room.is_available = True
        room.save()
