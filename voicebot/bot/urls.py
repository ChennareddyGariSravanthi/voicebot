# bot/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('setup/', views.setup_sdk, name='setup_sdk'),
    path('stream/', views.start_streaming, name='stream'),
]
