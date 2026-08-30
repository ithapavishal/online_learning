from functools import wraps
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from cart.models import Course, Enrollment


def user_is_enrolled(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        course_id = kwargs.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Check if the user is enrolled in the course
        is_enrolled = Enrollment.objects.filter(
            payment__student=request.user, course=course, is_enroll=True).exists()

        # Check if the user is the teacher of the course
        is_teacher = course.created_by == request.user

        if not is_enrolled and not is_teacher:
            return HttpResponseForbidden("You are not enrolled in this course and are not the teacher.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
