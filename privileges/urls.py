from django.urls import re_path
from privileges import views

app_name = 'privileges'

urlpatterns = [
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^user/profile/$', views.profile, name='profile'),
    re_path(r"^logout/$", views.logout, name='logout'),
    re_path(r'^helpPage/$', views.helpPage, name='helpPage'),
    re_path(r'^introduction/$', views.introduction, name='introduction')
]