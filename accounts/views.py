from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
from django.db import DatabaseError

class RegisterView(APIView):
    '''View to handle new user registration'''
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as db_error:
            return Response(
                {"error": "Database error occurred.", "details": str(db_error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LoginView(APIView):
    '''View to handle  user login'''
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        try:
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(username=username, password=password)
                if user:
                    refresh = RefreshToken.for_user(user)
                    user_data = {
                        "id": user.id,
                        "username": user.username,
                    }
                    return Response({
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "user": user_data,
                    }, status=status.HTTP_200_OK)
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except DatabaseError as db_error:
            return Response(
                {"error": "Database error occurred.", "details": str(db_error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            return Response(
                {"error": "Unexpected error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
