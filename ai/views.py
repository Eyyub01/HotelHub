from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from utils.permissions import IsOwnerOrReadOnly
from ai.models import AiResponse
from ai.serializers import AiResponseSerializer
from tasks import ai_for_hotel_and_room


class AiSupportRequestAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, room_id):
        ai_for_hotel_and_room.delay(room_id)
        return Response({'message': 'Request is being processed'}, status=status.HTTP_201_CREATED)


class AiSupportResponseAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def get(self, request, room_id):
        try:
            ai_response = AiResponse.objects.filter(room_id=room_id).latest('created_at')
            serializer = AiResponseSerializer(ai_response)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except AiResponse.DoesNotExist:
           return Response ({'message': 'No AI response found for this room.'}, status=status.HTTP_400_BAD_REQUEST)
    

