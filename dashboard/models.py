from django.db import models
from accounts.models import CustomUserModel
from django.core.validators import MinLengthValidator

# Create your models here.

# teacher Model


class TeacherProfile(models.Model):
    user = models.OneToOneField(
        CustomUserModel, on_delete=models.CASCADE, related_name='teacherprofile'
    )
    profile_img = models.ImageField(upload_to='profile_img')
    bio = models.TextField()
    age = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(
                10,
                message="Phone Number should be 10 charcter long",
            ),
        ],
    )


# student Model
class StudentProfile(models.Model):
    user = models.OneToOneField(
        CustomUserModel, on_delete=models.CASCADE, related_name='student_profile'
    )
    profile_img = models.ImageField(upload_to='profile_img')
    bio = models.TextField()
    age = models.PositiveIntegerField(default=0)
    address = models.CharField(max_length=200)
    goals = models.CharField(max_length=200, default='')
    phone_number = models.CharField(
        max_length=12,
        validators=[
            MinLengthValidator(
                10,
                message="Phone Number should be 10 charcter long",
            ),
        ],
    )
