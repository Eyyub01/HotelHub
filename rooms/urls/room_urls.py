from django.urls import path

from rooms.views.room_views import *

urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room_list'),
    path('room/create', CreateRoomAPIView.as_view(), name='room_create'),
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
]