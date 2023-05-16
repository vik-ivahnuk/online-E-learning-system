from django.urls import path
from . import views

urlpatterns = (
    path('', views.index, name='app'),
    path('home/', views.get_home, name='home'),
    path('home/course/<slug:code>/', views.get_course, name='course'),
    path('home/course/test/<slug:code>/', views.get_test, name='test'),
    path('home/teacher_mode', views.get_home_teacher, name='teacher'),
    path('home/teacher_mode/course_editor/<slug:code>/', views.get_course_editor, name='course_editor'),
    path('home/teacher_mode/course_editor/test/<slug:code>/', views.get_test_editor, name='test_editor')
)