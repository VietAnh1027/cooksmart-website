from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('admin-page/', views.admin_page, name='admin')
]