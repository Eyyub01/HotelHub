from django.urls import path

from rooms.views.room_photo_views import *


urlpatterns = [
    path('room/photos/<int:room_id>/', RoomPhotoAPIView.as_view(), name='room-photos'),
]