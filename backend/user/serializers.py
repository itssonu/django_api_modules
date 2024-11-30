from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'dob', 'profile_image']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            dob=validated_data.get('dob'),
            profile_image=validated_data.get('profile_image')
        )
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'dob', 'profile_image', 'created_at', 'updated_at']
        read_only_fields = ['email', 'created_at', 'updated_at']