from django.contrib import admin
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cate_title', 'created_by']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_title', 'created_by', 'category', 'price']


# vidoe
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']


# pdf
@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
