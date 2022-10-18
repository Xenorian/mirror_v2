from django import forms
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    confirm = forms.CharField(label="确认密码", min_length=6, max_length=18)

    class Meta:
        model = User
        fields = ['username', 'password', 'confirm']

    def clean_username(self):
        # 自定义用户名验证规则
        u_list = User.objects.filter(username=self.cleaned_data['username'])
        if len(u_list) > 0:
            raise forms.ValidationError("账号已存在，请使用其他账号注册")
        return self.cleaned_data['username']

    def clean_confirm(self):
        # 自定义确定密码验证规则
        if self.cleaned_data['password'] != self.cleaned_data['confirm']:
            raise forms.ValidationError("两次密码输入不一致")
        return self.cleaned_data['confirm']
