from django.db import models
from accounts.models import CustomUserModel
from online_learning_app.models import Course


# cart model
# Cart represents the overall course cart for a user.
class Cart(models.Model):
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart {self.id} for {self.user.username}'


# cartItem Model
# CartItem represents individual items within that cart.
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.course.course_title} in cart {self.cart.id}'


# payment model
class Payment(models.Model):
    student = models.ForeignKey(
        CustomUserModel, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(max_length=200)
    amount = models.FloatField()
    payment_status = models.CharField(max_length=200, default='')
    # Add this field to link payment to course
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid_at = models.DateTimeField()

    def __str__(self):
        return f'Payment {self.payment_id} for {self.amount}'


# enrollment model
class Enrollment(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name='enrollments'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enroll_at = models.DateTimeField(auto_now_add=True)
    is_enroll = models.BooleanField(default=False)

    def __str__(self):
        return f'Enrollment in {self.course.course_title} at {self.enroll_at}'
