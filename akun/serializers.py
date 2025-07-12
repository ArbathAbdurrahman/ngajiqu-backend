from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from .models import UserProfile

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer untuk registrasi user
    """
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all(),message="Email sudah terdaftar." )])
    password1 = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def validate_username(self, value):
        value = value.replace(" ", "").lower()
        if len(value) < 3:
            raise serializers.ValidationError("Username minimal 3 karakter")
        elif len(value) > 30:
            raise serializers.ValidationError("Username tidak boleh lebih dari 30 karakter")
        return value
    def validate_email(self, value):
        return value.strip()

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password2": "Password tidak sama."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1'],
        )
        return user
    
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email tidak ditemukan.")
        return value

class UserUpdateSerializer(serializers.ModelSerializer):
    """ Patch untuk model User """
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
        }

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """ Update Patch UserProfile """
    user = UserUpdateSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'description', 'profile_image', 'address', 'contact']
        extra_kwargs = {
            'description': {'required': False},
            'profile_image': {'required': False},
            'address': {'required': False},
            'contact': {'required': False},
        }

    def update(self, instance, validated_data):
        """
        Override metod update untuk menangani nested serializer.
        """
        user_data = validated_data.pop('user', {})
        user_instance = instance.user
        if user_data:
            user_serializer = UserUpdateSerializer(user_instance, data=user_data, partial=True)
            if user_serializer.is_valid(raise_exception=True):
                user_serializer.save()
        return super().update(instance, validated_data)