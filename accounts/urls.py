from django.urls import path  
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt import views 

from accounts.views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileListView.as_view(), name='profile'),
    
    path('api/token/', csrf_exempt(views.TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('api/token/refresh/', csrf_exempt(views.TokenRefreshView.as_view()), name='token_refresh'),
]