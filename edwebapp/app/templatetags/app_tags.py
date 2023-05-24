from django import template
from app.models import *

register = template.Library()


@register.inclusion_tag('app/courses.html')
def show_all_courses_teacher(username):
    user = User.objects.get(username=username)
    courses = Course.objects.filter(user=user).order_by('-created_at')
    return {
        'courses': courses,
        'is_student': False
    }


@register.inclusion_tag('app/courses.html')
def show_all_courses_student(username):
    user = User.objects.get(username=username)
    courses = Course.objects.filter(students__user=user, students__status='active').order_by('-students__joined_at')
    return {
        'courses': courses,
        'is_student': True
    }


@register.inclusion_tag('app/empty-block.html')
def show_empty_block_course(username, is_teacher):
    user = User.objects.get(username=username)

    if is_teacher:
        massage = 'У вас ще не має курсів. Створіть свій перший курс.'
        elements = Course.objects.filter(user=user)
    else:
        massage = 'У вас ще не має курсів. Приєднайтеся до курсу по коду який вам дасть ваш викладача'
        elements = Course.objects.filter(students__user=user, students__status='active').order_by('-students__joined_at')
    return {
        'is_empty': not elements.exists(),
        'massage': massage
    }



@register.inclusion_tag('app/header_authorized.html')
def show_header(username, name, is_home=False):
    return {
        'username': username,
        'name': name,
        'is_home': is_home
    }


@register.inclusion_tag('app/test-block.html')
def show_tests(course):
    tests = course.testmodel_set.order_by('-id')
    massage = 'Ви ще не створювали завдання.'
    is_empty = not tests.exists()
    return {
        'tests': tests,
        'is_teacher': True,
        'is_empty': is_empty,
        'massage': massage,
    }


@register.inclusion_tag('app/test-block.html')
def show_tests_student(course, username):
    tests = course.testmodel_set.filter(is_published=True).order_by('-id')
    massage = 'Тут ще немає завдань.'
    is_empty = not tests.exists()
    return {
        'tests': tests,
        'is_teacher': False,
        'username': username,
        'is_empty': is_empty,
        'massage': massage,
    }

@register.filter
def enumerate(sequence, start=1):
    return [(index + start, item) for index, item in enumerate(sequence)]
