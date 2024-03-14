# coindetection/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('webcam.html', views.webcam, name='webcam')
]
