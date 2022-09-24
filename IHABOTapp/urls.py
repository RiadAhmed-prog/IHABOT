from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from IHABOTapp import views

# from .views import TodoDetailApiView, TodoListApiView

urlpatterns = [
    path('api/get', views.get),
    path('api/post', views.post),
]
