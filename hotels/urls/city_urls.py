from django.urls import path, re_path
from hotels.views.city_views import CityListView, CityDetailView


urlpatterns = [
    path('cities/', CityListView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetailView.as_view(), name='city-detail'),
]
