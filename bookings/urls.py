from django.urls import path
from bookings.views import *

urlpatterns = [
    path('bookings/', UserBookingsListAPIView.as_view(), name='user-bookings'),
    path('booking/<int:room_id>/create', CreateBookingAPIView.as_view(), name='create-booking'),
    path('booking/<int:room_id>/detail', BookingDetailAPIView.as_view(), name='booking-detail')
]