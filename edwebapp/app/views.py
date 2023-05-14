from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *


def index(request):
    logout(request)

    if request.method == 'POST':
        print(request)
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
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'add_course_form': AddCourseForm()
    }

    if request.method == 'POST':
        if 'add_course' in request.POST:
            add_course_form = AddCourseForm(request.POST)
            if add_course_form.is_valid():
                code = add_course_form.cleaned_data.get('code')
                try:
                    course = Course.objects.get(code=code)
                except Course.DoesNotExist:
                    course = None
                if course is None:
                    print("Такого немає")
                    context = {
                        'username': request.user.username,
                        'name': request.user.first_name + ' ' + request.user.last_name,
                        'add_course_form': AddCourseForm()
                    }
                elif Student.objects.filter(user=request.user, course=course, status='active').exists():
                    print("Уже є")
                    context = {
                        'username': request.user.username,
                        'name': request.user.first_name + ' ' + request.user.last_name,
                        'add_course_form': AddCourseForm()
                    }
                try:
                    student = Student.objects.get(user=request.user, course=course, status='not_active')
                    student.status = 'active'
                    student.save()
                except Student.DoesNotExist:
                    student = Student()
                    student.user = request.user
                    student.course = course
                    student.save()
        elif 'delete_course' in request.POST:
            code = request.POST.get('delete_course')
            course = Course.objects.get(code=code)
            student = Student.objects.get(user=request.user, course=course)
            student.status = 'not_active'
            student.save()

    return render(request, 'app/home.html', context)


def get_course(request, code):
    course = get_object_or_404(Course, code=code)
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'course': course,
        'test_form': TestForm()
    }
    return render(request, 'app/course.html', context)


##### TODO
def get_test(request):
    context = {}
    return render(request, 'app/test-student.html', context)


def get_home_teacher(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST)
        if course_form.is_valid():
            course = Course()
            course.name = course_form.cleaned_data.get('name')
            course.description = course_form.cleaned_data.get('description')
            course.user = request.user
            course.save()

    context = {
        'course_form': CourseForm(),
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name
    }
    return render(request, 'app/home-teacher.html', context)


def get_course_editor(request, code):
    course = get_object_or_404(Course, code=code)
    if not course.user.username == request.user.username:
        return redirect('app')

    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'course': course,
        'test_form': TestForm()
    }
    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            name = test_form.cleaned_data.get('name')
            test = TestModel()
            test.name = name
            test.course = course
            test.save()

    return render(request, 'app/course_editor.html', context)


def get_test_editor(request, code):
    test = get_object_or_404(TestModel, code=code)
    context = {
        'test': test
    }
    return render(request, 'app/test_editor.html', context)
