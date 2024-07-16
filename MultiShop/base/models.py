from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .constant import GENDER_CHOICES, PROVINCE_CHOICES

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    father_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    city = models.CharField(max_length=50)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    about = models.TextField(max_length=500)
    profile_pic = models.ImageField(upload_to='profile_pic/')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return self.email
    
    def generate_verification_token(self):
        token = get_random_string(length=32)
        self.verification_token = token
        self.save()
        return token


@receiver(pre_delete, sender=User)
def delete_user_image(sender, instance, **kwargs):
    # Delete the image file associated with the user
    if instance.profile_pic:
        instance.profile_pic.delete(save=False)


