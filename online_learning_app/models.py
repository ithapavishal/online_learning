from django.db import models
from accounts.models import CustomUserModel
# Category


class Category(models.Model):
    '''
    this model is responsible for creating category
    '''
    cate_title = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name='category'
    )

    def __str__(self):
        return self.cate_title

# Course


class Course(models.Model):
    created_by = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name='courses'
    )
    course_image = models.ImageField(upload_to='course_image/')
    course_title = models.CharField(max_length=200)
    course_desc = models.CharField(max_length=200)
    category = models.ForeignKey(Category, related_name='course_category',on_delete=models.CASCADE)
    price = models.CharField(max_length=200)

    def __str__(self):
        return self.course_title

# PDF Model


class PDF(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='pdfs'
    )
    pdf_file = models.FileField(upload_to='course_pdfs/')
    title = models.CharField(max_length=200)
    pdf_des = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.title

#  video Model


class Video(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='videos')
    video_file = models.FileField(upload_to='course_videos/')
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title
