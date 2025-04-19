from django.urls import path
from .views import UserBookingsAPIView

urlpatterns = [
    path('bookings/', UserBookingsAPIView.as_view(), name='user-bookings'),
]