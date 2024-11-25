from django.contrib.auth.backends import BaseBackend
from .models import login

class LoginModelBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = login.objects.get(username=username)
            if user.password == password:
                return user
        except login.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return login.objects.get(pk=user_id)
        except login.DoesNotExist:
            return None