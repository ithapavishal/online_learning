from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def user_is_teacher(function):
    @login_required(login_url='/accounts/log_in/')
    def wrap(request, *args, **kwargs):
        if request.user.is_teacher:
            return function(request, *args, **kwargs)
        else:
            # Redirect to the home page if the user is not a teacher
            return redirect('home')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_student(function):
    @login_required(login_url='/accounts/log_in/')
    def wrap(request, *args, **kwargs):
        if not request.user.is_teacher:
            return function(request, *args, **kwargs)
        else:
            # Redirect to the home page if the user is not a student
            return redirect('home')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
