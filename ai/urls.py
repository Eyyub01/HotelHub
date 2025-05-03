from django.urls import path
from .views import AiSupportRequestAPIView, AiSupportResponseAPIView

urlpatterns = [
    path('support/request/<int:room_id>/', AiSupportRequestAPIView.as_view(), name='ai-support-request'),
    path('support/response/<int:room_id>/', AiSupportResponseAPIView.as_view(), name='ai-support-response'),
]
