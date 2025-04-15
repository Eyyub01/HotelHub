from django.urls import path

from hotels.views.hotel_views import(
    HotelListCreateAPIView, HotelRetrieveUpdateDestroy
)


urlpatterns = [
    path(
        'hotels/', 
        HotelListCreateAPIView.as_view(), 
        name='hotels'
    ),
    path(
        'hotels/<int:pk>/', 
        HotelRetrieveUpdateDestroy.as_view(),
        name='hotel_detail'
    ),
]
