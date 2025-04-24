from django.urls import path  
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from rest_framework_simplejwt import views 

from accounts.views import *

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('verify/', VerifyEmailAPIView.as_view(), name='verify'),
    path('login/', LoginAPIView.as_view(), name='login' ),
    path('logout/', LogoutAPIView.as_view(), name='logout' ),
    path('profiles/', OwnerListAPIView.as_view(), name='owner-profiles'),
    path('users/', UserListAPIView.as_view(), name='all-users'),
    path('profile/<int:profile_id>/', ProfileDetailAPIView.as_view(), name='profile-detail'),
    path('profile/update/', ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('profile/<int:profile_id>/hotels/', HotelsForOwnerAPIView.as_view(), name='hotels-for-owner'),
    
    path('api/token/', csrf_exempt(views.TokenObtainPairView.as_view()), name='token-obtain-pair'),
    path('api/token/refresh/', csrf_exempt(views.TokenRefreshView.as_view()), name='token-refresh'),

    path('register-form/', lambda request: render(request, 'accounts/registration.html'), name='register-form'),
    path('verify-form/', lambda request: render(request, 'accounts/verification.html'), name='verify-form'),
]