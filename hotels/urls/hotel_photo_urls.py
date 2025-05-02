from django.urls import path

from hotels.views.hotel_photo_views import *


urlpatterns = [
    path('hotels/<int:hotel_id>/photos/', HotelPhotoAPIView.as_view(), name='hotel-photo-list-create'),
    path('hotels/<int:hotel_id>/photos/<int:photo_id>/', HotelPhotoAPIView.as_view(), name='hotel-photo-delete'),
]