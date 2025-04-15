from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction 

from accounts.serializers import *
from utils.permissions import  HeHasPermission, IsOwnerOrReadOnly, IsEmailVerified
from utils.pagination import CustomPagination
from hotels.models.hotel_models import Hotel
from hotels.serializers.hotel_serializer import HotelSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        serializer = CustomerUserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                serializer.save()
                return Response(
                    {'message': 'User registered successfully. If you requested Owner role, it will be reviewed.'},
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        user = CustomUser.objects.get(email=email)
        if user.verification_code == code:
            user.email_verified = True
            user.verification_code = None
            user.save(update_fields=["email_verified", "verification_code"])
            return Response({'detail': 'Email verified successfully!'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission, IsEmailVerified]
    
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)

class OwnerRequestApprovalAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]  

    def post(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        if not user.is_owner_requested:
            return Response(
                {'error': 'This user has not requested Owner role.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.role = CustomUser.OWNER
        user.is_owner_requested = False
        user.save()
        serializer = CustomerUserSerializer(user)
        return Response(
            {'message': 'User promoted to Owner role.', 'data': serializer.data}, status=status.HTTP_200_OK
        )


class ProfileUpdateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission, IsEmailVerified]
   
    def patch(self, request):
        user = request.user
        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Profile updated successfully.', 'data': serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OwnerListAPIView(APIView):
    permission_classes = [AllowAny]  
    pagination_class = CustomPagination

    def get(self, request):
        pagination = self.pagination_class()
        owners = CustomUser.objects.filter(role=CustomUser.OWNER)
        if owners.exists():
            result_page = pagination.paginate_queryset(owners, request)
            serializer = CustomerUserSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'There are not any owners'}, status=status.HTTP_404_NOT_FOUND)
        


class UserListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]  

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomerUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HotelsForOwnerAPIView(APIView):
    permission_classes = [AllowAny]
    pagination_class = CustomPagination

    def get(self, request, profile_id):
        pagination = self.pagination_class()
        profile = get_object_or_404(CustomUser, id=profile_id)
        hotels = Hotel.objects.filter(owner=profile)
        if hotels.exists():
            result_page = pagination.paginate_queryset(hotels, request)
            serializer = HotelSerializer(result_page)
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'There are not any hotels'}, status=status.HTTP_404_NOT_FOUND)


class ProfileDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsEmailVerified]
    
    def get(self, request, profile_id):
        profile = get_object_or_404(CustomUser, id=profile_id)
        serializer = CustomerUserSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, profile_id):
        user_id = request.user.id
        profile = get_object_or_404(CustomUser, id=profile_id)
        serializer = CustomerUserSerializer(profile, data=request.data, partial=True)
        if user_id == profile_id:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, profile_id):
        user_id = request.user.id
        profile = get_object_or_404(CustomUser, id=profile_id)
        if user_id == profile_id:
            profile.delete()
            return Response({'message': 'User account deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'You do not have permission for this action'}, status=status.HTTP_403_FORBIDDEN)
        

    