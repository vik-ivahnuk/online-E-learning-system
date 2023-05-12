from django.contrib.auth.backends import ModelBackend
from .models import User


class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            if user.check_password(password) is True:
                return user
        except User.DoesNotExist:
            pass
