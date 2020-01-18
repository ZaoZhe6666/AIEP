from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from . import models
# Create your views here.

from . import forms


def register(request):
    if request.session.get('is_login', None):
        return render(request, 'index.html')
    if request.method == "POST":
        register_form = forms.RegisterForm(data=request.POST)
        message = "所有字段都必须填写"
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:
                message = "两次输入的密码不同"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.Profile.objects.filter(username=username)
                if same_name_user:
                    message = '用户已存在，请重新选择用户名!'
                    return render(request, 'register.html', locals())
                same_email_user = models.Profile.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱地址已被注册，请使用别的邮箱!'
                    return render(request, 'register.html', locals())
            """满足以上条件，创建新用户"""
            new_user = models.Profile.objects.create(
                username=username,
                password=make_password(password1, None, 'pbkdf2_sha256'),
                email=email,
            )
            return render(request, 'welcome.html')
        else:
            message = "不符合要求，请检查"
    register_form = forms.RegisterForm()
    return render(request, 'register.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return render(request, 'index.html')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = "所有字段都必须填写"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            same_name_user = models.Profile.objects.filter(username=username)
            if not same_name_user:
                message = "用户不存在或密码错误"
                return render(request, 'login.html', locals())
            if not check_password(password, same_name_user[0].password):
                message = "用户不存在或密码错误"
                return render(request, 'login.html', locals())
            request.session['is_login'] = True
            request.session['user_id'] = same_name_user[0].id
            request.session['user_name'] = same_name_user[0].username
            return render(request, 'welcome.html')
        return render(request, 'login.html', locals())
    login_form = forms.UserForm()
    return render(request, 'login.html', locals())


def logout(request):
    if request.session.get('is_login', None):
        request.session.flush()
    return render(request, 'index.html')
