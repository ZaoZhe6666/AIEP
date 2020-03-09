from django.shortcuts import render, HttpResponse, get_object_or_404
from .forms import RegistrationForm, LoginForm, PwdChangeForm
from .models import UserProfile
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def profile(request):
    user = get_object_or_404(User, pk=request.user.id)
    user_profile = get_object_or_404(UserProfile, user=user)
    if request.method == 'POST' and 'profile_change' in request.POST:
        user_profile.org = request.POST.get('org')
        user_profile.telephone = request.POST.get('telephone')
        user_profile.avatar = request.POST.get('avatar')
        user_profile.save()
        return render(request, 'profile.html', {
            'telephone': user_profile.telephone,
            'org': user_profile.org,
            'avatar': user_profile.avatar})
    elif request.method == 'POST' and 'password_change' in request.POST:
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        username = user.username
        user = auth.authenticate(username=username, password=old_password)
        if user is not None and user.is_active:
            if password1 == password2 and 6 < len(password1) < 18:
                user.set_password(password1)
                user.save()
                return HttpResponseRedirect('/privileges/login/')
            else:
                return render(request, 'profile.html', {
                    'user_profile': user_profile,
                    'user': user,
                    'message': '两次密码不一致或密码长度小于6'})
        else:
            return render(request, 'profile.html', {
                'user_profile': user_profile,
                'user': user,
                'message': 'Old password is wrong Try again'})
    else:
        return render(request, 'profile.html', {'telephone': user_profile.telephone, 'org': user_profile.org})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            # 使用内置User自带create_user方法创建用户，不需要使用save()
            user = User.objects.create_user(username=username, password=password, email=email)
            # 如果直接使用objects.create()方法后不需要使用save()
            user_profile = UserProfile.objects.create(user=user)
            return HttpResponseRedirect("/privileges/login/")
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                """
                使用该方法后，会在服务器端的session中生成_auth_user_id和_auth_user_backend两个键值，
                并发到客户端作为cookie，前端页面可通过{% if request.user.is_authenticated %}
                判断是否登录，来实现登录状态的保持功能。
                """
                return HttpResponseRedirect(reverse('privileges:profile'))
            else:
                # 登录失败
                return render(request, 'login.html',
                              {'form': form, 'message': 'Account does not exist or Wrong password, Please Try again'})
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/privileges/login/")


def help(request):
    return render(request, 'help.html', )


def introduction(request):
    return render(request, 'introduction.html')


def setup(request):
    return render(request, 'setup.html')


def contactUs(request):
    return render(request, 'contactUs.html')


def submit_avatar(request):
    pass
