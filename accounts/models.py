from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserModel(AbstractUser):
    gender = models.CharField(max_length=200)
    is_teacher = models.BooleanField(default=False)

# Create your models here.

