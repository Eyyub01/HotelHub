from django.urls import path

from favorites.views import *

urlpatterns = [
    path('favorites/', FavoriteListAPIView.as_view(), name='favorite-list'),
    path('favorite/<int:favorite_id>/', FavoriteDetailAPIView.as_view(), name='favorite-detail'),
    path('favorite/room/<int:room_id>/create/', CreateFavoriteForRoomAPIView.as_view(), name='create-favortie-room'),
    path('favorite/hotel/<int:hotel_id>/create/', CreateFavoriteForHotelAPIView.as_view(), name='create-favortie-hotel'),
]
