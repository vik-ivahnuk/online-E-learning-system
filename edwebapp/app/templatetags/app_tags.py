from django import template
from app.models import *

register = template.Library()


@register.inclusion_tag('app/teacher_courses.html')
def show_all_courses_teacher(username):
    user = User.objects.get(username=username)
    courses = Course.objects.filter(user=user)
    return {'courses': courses}


@register.inclusion_tag('app/header_authorized.html')
def show_header(username, name, is_home=False):
    return {
        'username': username,
        'name': name,
        'is_home': is_home
    }
