from django.shortcuts import render, redirect
from .models import CustomUserModel
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout

import re

# Create your views here.


def is_complex_password(password):
    '''
    This function is check complexity of the password enter by user
    '''
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    regex = re.compile(pattern)
    if regex.match(password):
        return True
    else:
        return False


def validate_registration(username, email, password, con_password):
    '''
    This function if use to validate register input value
    '''
    try:
        if password != con_password:
            return "Passwords do not match."

        if not is_complex_password(con_password):
            return "Password must be at least 8 characters and include uppercase, lowercase, digit, and special character."

        if CustomUserModel.objects.filter(username=username).exists():
            return "Username already exists."

        if CustomUserModel.objects.filter(email=email).exists():
            return "Email already exists."

    except Exception as e:
        print(f"Error: {str(e)}")


def choices(request):
    '''

    This choices view will get one choices for registration
    either for student or for instructor

    '''
    if request.method == 'POST':
        if 'teacher' in request.POST:
            request.session['user_type'] = 'teacher'
            return redirect('registration')

        elif 'student' in request.POST:
            request.session['user_type'] = 'student'
            return redirect('registration')

        else:
            return redirect('choices')

    return render(request, 'accounts/choices.html')


def registration(request):
    user_type = request.session.get('user_type')
    print(user_type, type(user_type))

    if user_type == 'teacher':
        is_teacher = True
    else:
        is_teacher = False

    if request.method == 'POST':
        data = request.POST
        firstname = data['firstname']
        lastname = data['lastname']
        username = data['username']
        email = data['email']
        selected_gender = request.POST.get('gender', None)
        password = data['password']
        con_password = data['con_password']

        message_text = validate_registration(
            username=username, email=email, con_password=con_password, password=password
        )

        messages.error(request, message_text)

        if not message_text:
            # Create user if all checks pass
            user = CustomUserModel.objects.create_user(
                first_name=firstname,
                last_name=lastname,
                username=username,
                email=email,
                gender=selected_gender,
                password=con_password,
                is_teacher=is_teacher,
            )

            return redirect('log_in')

    return render(request, 'accounts/registration.html', {'user_type': user_type})


def log_in(request):
    '''
    This function is responsible for login
    '''

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if not CustomUserModel.objects.filter(username=username).exists():
            messages.error(request, 'User is not register')
            return redirect('log_in')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_teacher:
                return redirect('dashboard')
            else:
                return redirect('home')

        else:
            messages.info(request, 'Invalid keyword')
            return redirect('log_in')

    return render(request, 'accounts/login.html')


def log_out(request):
    logout(request)
    return redirect('log_in')
