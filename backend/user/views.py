# views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import User

class RegisterView(APIView):
    def post(self, request):
        try:
            a = request.data.get('email')
            if User.objects.filter(email=request.data.get('email')).exists():
                return Response({
                    'message': 'User with this email already exists',
                    'statusCode': status.HTTP_400_BAD_REQUEST,
                    'success': False,
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = UserRegistrationSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                token = RefreshToken.for_user(user)
                
                return Response({
                    'message': 'User created successfully',
                    'statusCode': 201,
                    'success': True,
                    'data': {
                        'user': UserProfileSerializer(user).data,
                        'refreshToken': str(token),
                        'accessToken': str(token.access_token)
                    }
                }, status=status.HTTP_201_CREATED)
            
            return Response({
                'message': 'Validation error',
                'statusCode': 400,
                'success': False,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'message': str(e),
                'statusCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'success': False,
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            if not email or not password:
                return Response({
                    'message': 'Please provide both email and password',
                    'statusCode': 400,
                    'success': False,
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = authenticate(email=email, password=password)
            
            if user:
                token = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'statusCode': 200,
                    'success': True,
                    'data': {
                        'user': UserProfileSerializer(user).data,
                        'refreshToken': str(token),
                        'accessToken': str(token.access_token)
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message': 'Invalid credentials',
                'statusCode': 401,
                'success': False,
                'data': None
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        except Exception as e:
            return Response({
                'message': str(e),
                'statusCode': 500,
                'success': False,
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refreshToken = request.data.get('refresh_token')

            if not refreshToken:
                return Response({
                    'message': 'refresh token is required',
                    'statusCode': 400,
                    'success': False,
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refreshToken)

            return Response({
                    'message': 'Token refreshed successfully',
                    'statusCode': 200,
                    'success': True,
                    'data': {
                        'access_token': str(token.access_token)
                    }
                }, status=status.HTTP_200_OK)
            
            

        except Exception as e:
            return Response({
                'message': str(e),
                'statusCode': 500,
                'success': False,
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = UserProfileSerializer(request.user).data
            if user['profile_image']:
                user['profile_image'] = request.build_absolute_uri(user['profile_image'])
            return Response({
                'message': 'Profile retrieved successfully',
                'statusCode': 200,
                'success': True,
                'data': {
                    'user': user
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'message': str(e),
                'statusCode': 500,
                'success': False,
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'message': 'Profile updated successfully',
                    'statusCode': 200,
                    'success': True,
                    'data': {
                        'user': serializer.data
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                'message': 'Validation error',
                'statusCode': 400,
                'success': False,
                'data': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'message': str(e),
                'statusCode': 500,
                'success': False,
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)