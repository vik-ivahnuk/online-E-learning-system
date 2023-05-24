from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='app'),
    path('home/', views.get_home, name='home'),
    path('home/course/<slug:code>/', views.get_course, name='course'),
    path('home/course/test/<slug:code>/', views.get_test, name='test'),
    path('home/course/test/result/<slug:code>/', views.get_test_result, name='test_result'),
    path('home/teacher_mode', views.get_home_teacher, name='teacher'),
    path('home/teacher_mode/course_editor/<slug:code>/', views.get_course_editor, name='course_editor'),
    path('home/teacher_mode/course_editor/students/<slug:code>/', views.get_student_list, name='student_list'),
    path('home/teacher_mode/course_editor/test/<slug:code>/', views.get_test_editor, name='test_editor'),
    path('home/teacher_mode/course_editor/test/publish/<slug:code>/', views.get_test_publish, name='test_publish'),
    path('home/teacher_mode/course_editor/test/statistic/<slug:code>/', views.get_test_statistic, name='test_statistic')
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)