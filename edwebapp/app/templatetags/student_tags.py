from django import template
from app.models import *


register = template.Library()

@register.simple_tag
def get_status(test, username):
    user = User.objects.get(username=username)
    try:
        test_student = TestStudent.objects.get(test=test, student=user)
        if test_student.submitted_on_time:
            return 'здано'
        else:
            return 'здано з запізненням'
    except TestStudent.DoesNotExist:
        return 'термін здачі: ' + test.deadline.strftime('%Y-%m-%d %H:%M')



@register.simple_tag
def get_score(test, username):
    user = User.objects.get(username=username)
    try:
        test_student = TestStudent.objects.get(test=test, student=user)
        if test_student.submitted_on_time:
            return str(test_student.scores) + ' / ' + str(test_student.total_score)
        else:
            return str(test_student.scores) + ' / ' + str(test_student.total_score)
    except TestStudent.DoesNotExist:
        return ''

