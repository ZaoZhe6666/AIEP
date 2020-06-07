from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('submit/', views.submit, name='submit'),
    path('submit_check/', views.submit_check, name='submit_check'),
    path('404/', views.page_not_found, name='page_not_found'),
    path('waiting/', views.waiting, name='waiting'),
    path('queryAllResult/)', views.showline, name='showline'),
    url(r'^queryAllResult/([0-9]{4}_[0-9]{2}_[0-9]{2})/$', views.show_result, name='showline'),
    url(r'^queryAllResult/([0-9]{4}_[0-9]{2}_[0-9]{2}-[0-9]{6})/$', views.show_result, name='showline'),
    path('ajax/load_menu/', views.ajax_load_menu, name='ajax_load_menu'),
]