from rest_framework import serializers
from .models import CustomerUser

class CustomerUserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    is_owner_requested = serializers.BooleanField(default=False)

    class Meta:
        model = CustomerUser
        fields = ['username', 'email', 'password', 'phone_number', 'is_owner_requested']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'phone_number': {'required': False}
        }

    def validate_email(self, value):
        if CustomerUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = CustomerUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone_number=validated_data.get('phone_number', ''),
            is_owner_requested=validated_data.get('is_owner_requested', False)
        )
        return user