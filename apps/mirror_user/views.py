from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from . import forms
from django.contrib.auth.models import User


# Create your views here.
def user_login(request):
    if request.method == 'GET':
        return render(request, 'mirror_user/login.html', {})
    elif request.method == 'POST':
        # 接受登陆数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证表单数据
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect(reverse("board:projects", args=(user.get_username(),)))
        else:
            return render(request, 'mirror_user/login.html', {'msg_code': "-1", "msg_info": "账号或密码有误"})


def user_logout(request):
    logout(request)
    return redirect(reverse("mirror_user:user_login"))


def user_register(request):
    if request.method == "GET":
        return render(request, "mirror_user/register.html", {})
    elif request.method == "POST":
        # 接受用户注册数据
        form_register = forms.UserRegisterForm(request.POST)
        if form_register.is_valid():
            # 验证通过，创建用户对象
            User.objects.create_user(username=form_register.instance.username, password=form_register.instance.password, email=request.POST.get('email'))
            # 跳转到到登陆页面
            return redirect(reverse("mirror_user:user_login"), kwargs={"msg_code": "0", "msg_info": "注册成功"})
        else:
            return render(request, "mirror_user/register.html", {"form": form_register, "msg_code": "-1", "msg_info": "注册失败"})


def user_registerterms(request):
    return render(request, 'mirror_user/register_terms.html')


def user_forgetpassword(request):
    return render(request, 'mirror_user/forget_password.html')


def user_recoverpassword(request):
    if request.method == "GET":
        return render(request, 'mirror_user/recover_password.html')
    elif request.method == "POST":
        # 接受用户注册数据
        try:
            user = User.objects.get(username=request.POST.get('username'))
            if request.POST.get('password') == request.POST.get('confirm'):
                user.password = request.POST.get('password')
                # 跳转到到登陆页面
                return redirect(reverse("mirror_user:user_login"), kwargs={"msg_code": "0", "msg_info": "密码修改成功"})
            else:
                return render(request, "mirror_user/recover_password.html", {"msg_code": "-1", "msg_info": "两次输入的密码不一致"})
        except:
            return render(request, "mirror_user/recover_password.html", {"msg_code": "-1", "msg_info": "用户不存在"})
