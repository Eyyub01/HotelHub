from django.urls import path
from hotels.views.hotel_views import HotelListView, HotelDetailView, HotelCreateView, HotelSearchAPIView

urlpatterns = [
    path('hotels/', HotelListView.as_view(), name='hotel-list'),
    path('hotels/create/', HotelCreateView.as_view(), name='create_hotel'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='detail_hotel'),
    path('hotels/search/', HotelSearchAPIView.as_view(), name='hotel_search')
]
