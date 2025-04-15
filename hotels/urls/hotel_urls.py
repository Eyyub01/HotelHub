from django.urls import path
<<<<<<< HEAD
from hotels.views.hotel_views import *
=======
from hotels.views.hotel_views import HotelListView, HotelDetailView, HotelCreateView, HotelSearchAPIView
>>>>>>> development

urlpatterns = [
    path('hotels/', HotelListView.as_view(), name='hotel-list'),
    path('hotels/create/', HotelCreateView.as_view(), name='create_hotel'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(), name='detail_hotel'),
<<<<<<< HEAD
    path('hotels/search/', HotelSearchAPIView.as_view(), name='hotel_search'),
    path('hotels/filter/', HotelFilterAPIView.as_view(), name='hotel_filter'),
=======
    path('hotels/search/', HotelSearchAPIView.as_view(), name='hotel_search')
>>>>>>> development
]
