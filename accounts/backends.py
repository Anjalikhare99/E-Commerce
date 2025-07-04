from django.contrib.auth.backends import ModelBackend
from .models import *

class EmailOrPhoneBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            try:
                user = User.objects.get(phone_number=username)
            except User.DoesNotExist:
                return None
        except User.MultipleObjectsReturned:
            return None

        if user and user.check_password(password):
            return user
        return None