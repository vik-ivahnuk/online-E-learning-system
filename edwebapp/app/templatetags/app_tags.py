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
    return {
        'tests': tests,
        'is_teacher': True
    }


@register.inclusion_tag('app/test-block.html')
def show_tests_student(course, username):
    tests = course.testmodel_set.order_by('-id')
    return {
        'tests': tests,
        'is_teacher': False,
        'username': username
    }






