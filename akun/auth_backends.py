from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """ 
    Custom auth untuk login menggunakan email 
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get("email") or username
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None
