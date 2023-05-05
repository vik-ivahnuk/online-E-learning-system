from django.urls import path
from . import views

urlpatterns = (
    path('', views.index),
    path('home', views.get_home, name='home')
)
