from django.contrib import admin
from .models import CustomUserModel

# Register your models here.


@admin.register(CustomUserModel)
class CustomUserModel(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'gender',
        'email',  'is_teacher',
    ]
    search_fields = ['first_name']
