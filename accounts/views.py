from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomerUserRegisterSerializer

class ProfileListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = CustomerSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class RegisterView(APIView):
    permission_classes = []  
    def post(self, request):
        serializer = CustomerUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'User registered successfully. If you requested Owner role, it will be reviewed.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)