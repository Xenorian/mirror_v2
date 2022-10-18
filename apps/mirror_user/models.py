from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserProfile(models.Model):
    C_GENDER = (
        ('0', '女'),
        ('1', '男')
    )
    # 用户
    user = models.OneToOneField(verbose_name="用户", to=User, related_name="profile", on_delete=models.CASCADE)
    # 性别
    gender = models.CharField(max_length=5, verbose_name="性别", choices=C_GENDER, default='1')
    # 年龄
    age = models.IntegerField(verbose_name="年龄", default=0)
    # 手机
    phone = models.CharField(max_length=15, verbose_name="手机", null=True, blank=True)
    # 组织
    org = models.CharField(verbose_name="组织", max_length=200, null=True, blank=True)
    # 简介
    intro = models.TextField(verbose_name="简介", null=True, blank=True)
    # 邮箱验证码
    verification = models.CharField(max_length=5, verbose_name="验证码", default="0", null=True, blank=True)  


class UserContact(models.Model):
    # 用户
    user = models.ForeignKey(verbose_name="用户", to=User, related_name="contact", on_delete=models.CASCADE)
    # 主题
    theme = models.TextField(verbose_name="主题", null=True, blank=True)
    # 信息
    info = models.TextField(verbose_name="信息", null=True, blank=True)

    realname = models.CharField(max_length=15, verbose_name="真实姓名", null=True, blank=True)

    email = models.EmailField(null=True, blank=True)
