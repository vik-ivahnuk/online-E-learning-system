from django.contrib import admin
from .models import *

admin.site.register(User)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'description', 'created_at', 'user')


admin.site.register(Course, CourseAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('joined_at', 'status', 'course', 'user')


admin.site.register(Student, StudentAdmin)

admin.site.register(TestModel)
