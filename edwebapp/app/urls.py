from django.urls import path
from . import views

urlpatterns = (
    path('', views.index, name='app'),
    path('home/', views.get_home, name='home'),
    path('home/course', views.get_course, name='course'),
    path('home/teacher_mode', views.get_home_teacher, name='teacher'),
    path('home/teacher_mode/course_editor/<slug:code>/', views.get_course_editor, name='course_editor')
)