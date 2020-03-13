from django.urls import re_path
from privileges import views

app_name = 'privileges'

urlpatterns = [
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^login/$', views.login, name='login'),
    re_path(r'^user/profile/$', views.profile, name='profile'),
    re_path(r"^logout/$", views.logout, name='logout'),
    re_path(r'^help/$', views.help, name='help'),
    re_path(r'^introduction/$', views.introduction, name='introduction'),
    re_path(r'^setup/$', views.setup, name='setup'),
    re_path(r'^contactUs/$', views.contactUs, name='contactUs'),
    re_path(r'^submit_avatar/$', views.submit_avatar, name='submit_avatar'),
    re_path(r'^get_avatar_url/$', views.get_avatar_url, name='get_avatar_url'),
    re_path(r'^Data_Information1/$', views.Data_Information1, name='Data_Information1'),
    re_path(r'^Data_Information2/$', views.Data_Information2, name='Data_Information2'),
]
