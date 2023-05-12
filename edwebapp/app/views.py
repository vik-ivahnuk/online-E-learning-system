from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    logout(request)

    if request.method == 'POST':
        if 'sign-up' in request.POST:
            signupform = SignUpForm(request.POST)
            signinform = SignInForm()
            num = 2
            if signupform.is_valid():
                signupform.save()
                username = signupform.cleaned_data.get('username')
                raw_password = signupform.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password, backend='app.backends.UserBackend')
                print(user)
                login(request, user)
                if request.user.is_authenticated:
                    return redirect('home')
        else:
            signinform = SignInForm(request.POST)
            signupform = SignUpForm()
            num = 1
            if signinform.is_valid():
                username = signinform.cleaned_data.get('username')
                raw_password = signinform.cleaned_data.get('password')
                user = authenticate(username=username, password=raw_password)
                if user is None:
                    signinform.add_error(None, 'Неправильне ім\'я користувача або пароль.')
                else:
                    login(request, user)
                    return redirect('home')
    else:
        signupform = SignUpForm()
        signinform = SignInForm()
        num = 0
    context = {
        'signupform': signupform,
        'signinform': signinform,
        'mode': num
    }

    return render(request, 'app/login-page.html', context)


@login_required(login_url='/')
def get_home(request):
    # print(request.user.courses.all())
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name
    }
    return render(request, 'app/home.html', context)


def get_course(request):
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'test_form': TestForm()
    }
    return render(request, 'app/course.html', context)


@login_required(login_url='home')
def get_home_teacher(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = Course()
            course.name = course_form.cleaned_data.get('name')
            course.description = course_form.cleaned_data.get('description')
            course.user = request.user
            course.save()
            print('successfully')

    context = {
        'course_form': CourseForm(),
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name
    }
    return render(request, 'app/home-teacher.html', context)


def get_course_editor(request, code):
    course = Course.objects.get(code=code)
    context = {
        'course': course
    }
    return render(request, 'app/course.html', context)
