from django.urls import path  
from rest_framework_simplejwt import views 


urlpatterns = [
    path('api/token/', views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
]