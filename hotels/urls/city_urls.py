from django.urls import path, re_path
from hotels.views.city_views import CityListView, CityDetailView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Hotel API",
        default_version="v1",
        description="API documentation for the Hotel project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@hotelhub.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('cities/', CityListView.as_view(), name='city_list'),
    path('cities/<int:pk>/', CityDetailView.as_view(), name='city_detail'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
