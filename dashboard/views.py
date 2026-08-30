
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError

from online_learning_app.models import Course, Category
from .models import TeacherProfile, StudentProfile
from accounts.models import CustomUserModel
from .decorators import user_is_student, user_is_teacher
from cart.models import Enrollment
from quiz.models import StudentProgress, OverallProgress
from django.db.models import Sum


from cart.models import *


# Create your views here.

# dashboard


@user_is_teacher
def dashboard(request):
    courses = Course.objects.all()
    enroll_students = Enrollment.objects.all()
    context = {
        'courses': courses,
        'enroll_students': enroll_students
    }
    return render(request, 'dashboard/teacher/dashboard.html', context=context)

# notifications


@user_is_teacher
def notifications(request):
    return render(request, 'dashboard/teacher/notifications.html')

# ------------------------------------ Profile -------------------------------------------------
# profile


@user_is_teacher
def teacher_profile(request):
    return render(request, 'dashboard/teacher/profile.html')


# Update Teacher Profile


@user_is_teacher
def update_teacher_profile(request, id):
    teacher = get_object_or_404(CustomUserModel, id=id)
    if request.method == 'POST':
        profile_img = request.FILES.get('profile_image')
        age = request.POST.get('age')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        bio = request.POST.get('bio')

        errors = []

        # Validation
        if not phone_number.isdigit() or len(phone_number) < 10:
            errors.append(
                "Phone number must contain only digits and be at least 10 digits long"
            )

        if not errors:
            try:
                # Get or create the teacher profile linked to the current user
                teacher_profile, created = TeacherProfile.objects.get_or_create(
                    user=request.user
                )
                # Update the profile with new data
                teacher_profile.profile_img = profile_img
                teacher_profile.age = age
                teacher_profile.address = address
                teacher_profile.phone_number = phone_number
                teacher_profile.bio = bio
                teacher_profile.save()
                return redirect('profile')
            except ValidationError as e:
                errors.append(str(e))
        else:
            for error in errors:
                print(error)

    context = {
        'teacher': teacher,
    }

    return render(request, 'dashboard/teacher/update_teacher_profile.html', context=context)

# tables


@user_is_teacher
def courses_dashboard(request):
    courses = Course.objects.all()
    category = Category.objects.all()
    context = {
        'courses': courses,
        'category': category,
    }

    return render(request, 'dashboard/teacher/courses.html', context=context)


# student dashboard
@user_is_student
def student_dashboard(request):
    overall_progress = OverallProgress.objects.filter(user=request.user)
    student_progress = StudentProgress.objects.filter(user=request.user)

    # Aggregate the total score for the user
    total_score = overall_progress.aggregate(total=Sum('score'))['total']
    # Calculate the total number of questions across all quizzes the user has attempted
    total_questions = overall_progress.aggregate(
        total_questions=Sum('total_questions'))['total_questions']

    context = {
        'overall_progress': overall_progress,
        'student_progress': student_progress,
        'total_score': total_score,
        'total_questions': total_questions,
    }
    return render(request, 'dashboard/student/stu_dashboard.html', context=context)
# student profile


@user_is_student
def student_profile(request):
    return render(request, 'dashboard/student/stu_profile.html')

# update student profile


@user_is_student
def student_update_profile(request, id):
    student_id = get_object_or_404(CustomUserModel, id=id)
    errors = []

    if request.method == 'POST':
        stu_profile_img = request.FILES.get('profile_image')
        stu_age = request.POST.get('age')
        stu_address = request.POST.get('address')
        stu_phone_number = request.POST.get('phone_number')
        stu_goal = request.POST.get('goal')
        stu_bio = request.POST.get('bio')

        # Check if age is provided and is a valid integer
        try:
            stu_age = int(stu_age)
        except (TypeError, ValueError):
            errors.append("Age must be a valid number.")

        # Validate phone number
        if not stu_phone_number.isdigit() or len(stu_phone_number) < 10:
            errors.append(
                "Phone number must contain only digits and be at least 10 digits long.")

        if not errors:
            try:
                # Get or create the student profile linked to the current user
                student_profile, created = StudentProfile.objects.get_or_create(
                    user=request.user
                )
                # Update the profile with new data
                if stu_profile_img:
                    student_profile.profile_img = stu_profile_img
                student_profile.age = stu_age
                student_profile.address = stu_address
                student_profile.phone_number = stu_phone_number
                student_profile.goals = stu_goal
                student_profile.bio = stu_bio
                student_profile.save()
                return redirect('student_profile')
            except ValidationError as e:
                errors.append(str(e))

    context = {
        'student_id': student_id,
        'errors': errors
    }

    return render(request, 'dashboard/student/update_stu_profile.html', context=context)


@user_is_student
def enrollment_page(request):
    enroll_courses = Enrollment.objects.all()
    for enroll in enroll_courses:
        print(enroll)

    context = {
        'enroll_courses': enroll_courses,
    }
    return render(request, 'dashboard/student/enroll_course.html', context=context)
