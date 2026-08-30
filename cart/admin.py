from django.contrib import admin
from .models import *
# Register your models here.

# cart admin


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']


# cartItem admin
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'course', 'is_paid', 'added_at']

# Payment admin


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'course', 'amount',
        'payment_id', 'student', 'paid_at',
    ]

# Enrollment Admin


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'payment', 'course', 'enroll_at', 'is_enroll']
