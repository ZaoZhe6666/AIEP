from django import forms
from django.contrib.auth.models import User
import re
from captcha.fields import CaptchaField


def email_check(email):
    pattern = re.compile(r"\"?([-a-zA-Z0-9.'?{}]+@\w+\.\w+)\"?")
    return re.match(pattern, email)


class RegistrationForm(forms.Form):
    username = forms.CharField(label='username', max_length=50, widget=forms.TextInput(attrs={
       'class': "form-control input-lg", 'placeholder': 'Username', 'id': 'username'}))
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={
       'class': "form-control input-lg", 'placeholder': 'Email', 'id': 'email'}))
    password1 = forms.CharField(label='password1', widget=forms.PasswordInput(attrs={
       'class': "form-control input-lg", 'placeholder': 'Password', 'id': 'password1'}))
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput(attrs={
       'class': "form-control input-lg", 'placeholder': 'Password Confirmation', 'id': 'password2'}))
    # captcha = CaptchaField(label='验证码', error_messages={"invalid": "验证码错误"})
    # user clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError("your username must be at least 3 characters log")
        elif len(username) > 20:
            raise forms.ValidationError("your username is too long")
        else:
            filter_result = User.objects.filter(username__exact=username)
            if len(filter_result) > 0:
                raise forms.ValidationError('your username already exists')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email_check(email):
            filter_result = User.objects.filter(email__exact=email)
            if len(filter_result) > 0:
                raise forms.ValidationError("your email already exists")
        else:
            raise forms.ValidationError("Please enter a valid email")

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 6:
            raise forms.ValidationError("your password is too short")
        elif len(password1) > 20:
            raise forms.ValidationError("your password is too long")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch Please enter again')

        return password2


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=50, widget=forms.TextInput(attrs={
       'class': "form-control input-lg", 'placeholder': 'Username'}))
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={
       'class': "form-control input-lg", 'placeholder': 'Password'}))
    # captcha = CaptchaField(label='验证码', error_messages={"invalid": "验证码错误"})
    # use clean methods to define custom validation rules

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if email_check(username):
            filter_result = User.objects.filter(email__exact=username)
            if not filter_result:
                raise forms.ValidationError('This email does not exist')
        else:
            filter_result = User.objects.filter(username__exact=username)
            if not filter_result:
                raise forms.ValidationError('This username does not exist Please register first')

        return username


class PwdChangeForm(forms.Form):
    old_password = forms.CharField(
        label='Old Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "输入账号的原登录密码"
        }))
    password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "输入账号的原登录密码"
        }))
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "输入账号的原登录密码"
        }))

    # use clean methods to define custom validation rules

    def clean_password1(self):
        password1 = self.cleaned_data.get('Password')

        if len(password1) < 6:
            raise forms.ValidationError("your password is too short")
        elif len(password1) > 20:
            raise forms.ValidationError("your password is too long")

        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('Password')
        password2 = self.cleaned_data.get('Password confirmation')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password mismatch Please enter again")

        return password2
