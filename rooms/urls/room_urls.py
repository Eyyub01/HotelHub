from django.urls import path

from rooms.views.room_views import *

urlpatterns = [
    path('rooms/', RoomListAPIView.as_view(), name='room-list'),
    path('room/create', CreateRoomAPIView.as_view(), name='room-create'),
    path('room/<int:room_id>/', RoomDetailView.as_view(), name='room-detail'),
    path('rooms/<int:hotel_id>/hotel/', RoomsForHotelAPIView.as_view(), name='rooms-for-hotel'),
    path('rooms/search/', RoomElasticSearchAPIView.as_view(), name='rooms-search')
]