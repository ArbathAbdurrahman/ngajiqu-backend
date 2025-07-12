from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import status
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import *

class RegistrationView(APIView):
    """ Registrasi User """
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """ View untuk Login menggunakan email dan password """
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    """ Logout untuk user yang sedang login dan blacklist token """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ResetPasswordView(APIView):

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            # user = User.objects.get(email=email)

            reset_token = get_random_string(32)
            # Kirim email reset password
            reset_link = f"https://ngajiqu.teknohole.com/reset-password/{reset_token}"
            send_mail(
                "Reset Password",
                f"Klik link berikut untuk reset password: {reset_link}",
                "noreply@ngajiqu.com",
                [email],
                fail_silently=False,
            )
            return Response({'message': 'Silakan cek email untuk reset password'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """
    API View untuk melihat (GET) dan memperbarui (PATCH/PUT) profil pengguna
    
    * Hanya pengguna yang terautentikasi yang dapat mengakses endpoint ini
    * Pengguna hanya dapat melihat dan mengubah profil mereka sendiri
    * Mendukung metode GET, PUT, dan PATCH
    """
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)

