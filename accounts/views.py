from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.urls import reverse
from django.http import HttpResponseRedirect

from accounts.serializers import *
from utils.permissions import HeHasPermission, IsOwnerOrReadOnly, IsEmailVerified
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
                    {'message': 'User registered successfully.'},
                    status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        if user.email_verification_code == code:  # Use the correct field name
            user.is_email_verified = True  # Update the email verification status
            user.email_verification_code = None  # Clear the verification code
            user.save(update_fields=["is_email_verified", "email_verification_code"])
            return Response({'detail': 'Email verified successfully!'}, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid verification code.'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    """User login endpoint (public access)."""
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        except serializers.ValidationError as e:
            if 'account' in str(e):
                return HttpResponseRedirect(reverse('register'))
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
        return Response({'message': 'There are no owners.'}, status=status.HTTP_404_NOT_FOUND)


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
            serializer = HotelSerializer(result_page, many=True)
            return pagination.get_paginated_response(serializer.data)
        return Response({'message': 'There are no hotels.'}, status=status.HTTP_404_NOT_FOUND)


class ProfileDetailAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, profile_id):
        profile = get_object_or_404(CustomUser, id=profile_id)
        serializer = CustomerUserSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, profile_id):
        user_id = request.user.id
        profile = get_object_or_404(CustomUser, id=profile_id)
        if user_id != profile_id:
            return Response({'message': 'You do not have permission for this action.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = CustomerUserSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, profile_id):
        user_id = request.user.id
        profile = get_object_or_404(CustomUser, id=profile_id)
        if user_id != profile_id:
            return Response({'message': 'You do not have permission for this action.'}, status=status.HTTP_403_FORBIDDEN)

        profile.delete()
        return Response({'message': 'User account deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)