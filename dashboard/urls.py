from django.urls import path
from .views import *

urlpatterns = [
    # teacher dashboard
    path('dashboard/', dashboard, name="dashboard"),
    path('courses_dashboard/', courses_dashboard, name="courses_dashboard"),
    path('notifications/', notifications, name="notifications"),

    path('profile/', teacher_profile, name="profile"),
    path('update_teacher_profile/<int:id>', update_teacher_profile,
         name='update_teacher_profile'),


    # student dashboard
    path('student_dashboard/', student_dashboard, name='student_dashboard'),
    path('student_profile/', student_profile, name='student_profile'),
    path('student_update_profile/<int:id>', student_update_profile,
         name='student_update_profile'),
    path('enrollment/', enrollment_page, name='enrollment'),

]
