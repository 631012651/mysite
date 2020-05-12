
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from . import forms

from . import models

import hashlib

def hello(request):
    return HttpResponse("Hello world ! ")

def index(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')
    return render(request,'../templates/index.html')
'''
def login(request):
    pass
    return render(request,'../templates/login.html')
'''
def login(request):
    if request.session.get('is_login',None):
        return redirect('/index/')
    if request.method == 'POST':
        login_forms = forms.UserForm(request.POST)
        message = "所有字段都必须填写！"
        if login_forms.is_valid():
            username = login_forms.cleaned_data.get('username')
            password = login_forms.cleaned_data.get('password')


            try:
                user = models.User.objects.get(name=username)

            except:
                message = "用户不存在"
                return render(request,'../templates/login.html',locals())
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('/index/')
            else:
                message = "密码不正确"
                return render(request,'login/login.html',locals())

    login_form = forms.UserForm()
    return render(request,'../templates/login.html',locals())

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            email = register_form.cleaned_data.get('email')
            sex = register_form.cleaned_data.get('sex')
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, '../templates/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, '../templates/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, '../templates/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.User()
                new_user.name = username
                new_user.password = password1
                new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = forms.RegisterForm()
    return render(request, '../templates/register.html', locals())


def logout(request):
    if not request.session.get('is_login',None):
        return redirect('/login/')

    request.session.flush()
    return redirect('/login/')


    #return render(request, '../templates/login.html')



def hash_code(s,salt='mysite'):
    h=hashlib.sha256()
    s+=salt
    h.update(s.encode())
    return h.hexdigest()


