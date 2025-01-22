from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, blank=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    nickname = models.CharField(max_length=40, blank=True)
    intro = models.TextField(blank=True)