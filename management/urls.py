from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('submit/', views.submit, name='submit'),
    path('submit_check/', views.submit_check, name='submit_check'),
    path('404/', views.page_not_found, name='page_not_found'),
]