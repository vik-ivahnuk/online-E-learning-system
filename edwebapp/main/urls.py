from django.urls import path
from . import views

urlpatterns = (
    path('', views.index, name='main'),
    path('home/', views.get_home, name='home')
)
