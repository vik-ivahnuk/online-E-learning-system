from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import re
from . import utils

import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image
from django.core.files import File


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
                    context = {
                        'username': request.user.username,
                        'name': request.user.first_name + ' ' + request.user.last_name,
                        'add_course_form': AddCourseForm()
                    }
                elif Student.objects.filter(user=request.user, course=course, status='active').exists():
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


@login_required(login_url='/')
def get_course(request, code):
    course = get_object_or_404(Course, code=code)
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'course': course,
        'test_form': TestForm()
    }
    return render(request, 'app/course.html', context)


@login_required(login_url='/')
def get_test(request, code):
    test = TestModel.objects.get(code=code)
    tasks = Task.objects.filter(test=test)
    if TestStudent.objects.filter(test=test, student=request.user).exists():
        return redirect('test_result', code=code)

    if request.method == 'POST':
        student_test_set = request.POST.copy()
        test_student = TestStudent()
        test_student.test = test
        test_student.student = request.user
        num = 0
        total = 0
        for t in tasks:
            answers = Answer.objects.filter(task=t, is_correct=True)
            is_correct = True
            if len(answers) != len(student_test_set.getlist(f'{t.id}')):
                is_correct = False
            else:
                for answer in answers:
                    if (not str(answer.id) in student_test_set.getlist(f'{t.id}')) and answer.is_correct:
                        is_correct = False
                        break
            if is_correct:
                num += 1
            total += 1
            ans = AnswerStudent()
            ans.task = t
            ans.student = request.user
            ans.is_correct = is_correct
            ans.save()
        current_datetime = timezone.now()
        if current_datetime > test.deadline:
            test_student.submitted_on_time = False
            test_student.scores = 0
        else:
            test_student.submitted_on_time = True
            test_student.scores = num

        test_student.total_score = total
        test_student.save()
        return redirect('test_result', code=code)
    form = TestStudentForm(questions=tasks)
    context = {
        'test': test,
        'form': form,
    }

    return render(request, 'app/test-student.html', context)


def get_test_result(request, code):
    test = TestModel.objects.get(code=code)
    test_student = TestStudent.objects.get(test=test, student=request.user)

    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'score': test_student.scores,
        'total_score': test_student.total_score,
        'test': test
    }
    return render(request, 'app/test-result.html', context)


@login_required(login_url='/')
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


@login_required(login_url='/')
def get_course_editor(request, code):
    course = get_object_or_404(Course, code=code)
    if not course.user.username == request.user.username:
        return redirect('app')

    if request.method == 'POST':
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            name = test_form.cleaned_data.get('name')
            test = TestModel()
            test.name = name
            test.course = course
            test.save()
            return redirect('course_editor', code=code)
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'course': course,
        'test_form': TestForm()
    }
    return render(request, 'app/course_editor.html', context)


@login_required(login_url='/')
def get_student_list(request, code):
    course = get_object_or_404(Course, code=code)
    students = course.students.all()
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'students': students,
        'course_name': course.name,
        'is_empty': not students.exists()
    }
    return render(request, 'app/students_list.html', context)


@login_required(login_url='/')
def get_test_editor(request, code):
    test = get_object_or_404(TestModel, code=code)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        AnswerFormSet2 = formset_factory(AnswerForm)
        answer_prefix = 'answer'
        answer_formset_data = {k: v for k, v in request.POST.items() if
                               answer_prefix in k}
        num = sum(key.count('answer_text') for key in answer_formset_data.keys())
        answer_formset_data["answer-TOTAL_FORMS"] = f"{num}"
        cur = 0
        formset = {}
        for key, v in answer_formset_data.items():
            if 'answer-' in key and '-answer_text' in key:
                num = int(key.split('-')[1])
                if num - cur > 1:
                    num = cur + 1
                cur = num
                k = 'answer-' + str(num) + '-answer_text'
                formset[k] = v
            elif 'answer-' in key and '-is_correct' in key:
                num = int(key.split('-')[1])
                if num > cur:
                    k = 'answer-' + str(cur) + '-is_correct'
                    formset[k] = v
                else:
                    formset[key] = v
            else:
                formset[key] = v

        answers = AnswerFormSet2(formset, prefix=answer_prefix)
        if form.is_valid() and answers.is_valid():
            question_text = form.cleaned_data['question_text']
            img_svg = form.cleaned_data['hidden_input']

            task = Task()
            task.test = test
            task.question = question_text

            task.save()
            if len(img_svg) > 0:
                svg_data = img_svg.encode('utf-8')
                drawing = svg2rlg(io.StringIO(svg_data.decode()))
                png_data = renderPM.drawToString(drawing, fmt='PNG')

                image = Image.open(io.BytesIO(png_data))
                image_io = io.BytesIO()
                image.save(image_io, format='PNG')
                image_file = File(image_io)
                task.photo.save('image' + str(task.id) + '.png', image_file)
                task.save()

            for answer_form in answers:
                if answer_form.is_valid():
                    answer_text = answer_form.cleaned_data.get('answer_text')
                    is_correct = answer_form.cleaned_data.get('is_correct')
                    answer = Answer()
                    answer.text = answer_text
                    answer.is_correct = is_correct
                    answer.task = task
                    answer.save()
            return redirect('test_editor', code=code)

    form = QuestionForm()
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'test': test,
        'form': form,
        'is_published': test.is_published
    }
    return render(request, 'app/test-editor.html', context)


@login_required(login_url='/')
def get_test_publish(request, code):
    test = TestModel.objects.get(code=code)
    if request.method == 'POST':
        form = DateTimeForm(request.POST)
        if form.is_valid():
            test.deadline = form.cleaned_data['deadline']
            test.is_published = True
            test.save()
            return redirect('test_editor', code=code)

    form = DateTimeForm()
    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'form': form,
        'testname': test.name
    }
    return render(request, 'app/test-publish.html', context)


@login_required(login_url='/')
def get_test_statistic(request, code):
    test = TestModel.objects.get(code=code)
    course = test.course
    students = course.students.all()
    students_statistic = []
    for student in students:
        full_name = student.user.last_name + ' ' + student.user.first_name
        try:
            test_student = TestStudent.objects.get(student=student.user, test=test)
            status = 'Здано вчасно' if test_student.submitted_on_time else 'Здано не вчасно'
            score = str(test_student.scores) + ' / ' + str(test_student.total_score)
        except TestStudent.DoesNotExist:
            status = 'Не здано'
            score = ''
        students_statistic.append(utils.StudentStatistic(full_name, status, score))

    context = {
        'username': request.user.username,
        'name': request.user.first_name + ' ' + request.user.last_name,
        'test': test,
        'students_statistic': students_statistic
    }
    return render(request, 'app/test-statistic.html', context)


def get_exp(request):
    if request.method == 'POST':
        svg_code = request.POST.get('svgData')
    return render(request, 'app/exp.html')
