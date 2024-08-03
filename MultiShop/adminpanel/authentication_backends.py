from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models   

class SuperuserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()
        # Check if user exists by username or email
        user = User.objects.filter(models.Q(username=username) | models.Q(email=username)).first()
        if user and user.is_superuser and user.check_password(password):
            return user
        return None
