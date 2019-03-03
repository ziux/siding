from django.db import models
from instructor.models import Teacher
# Create your models here.
class Token(models.Model):
    token = models.CharField(verbose_name='token', max_length=255, primary_key=True)
    value = models.BinaryField(verbose_name='值', max_length=2555)
    expiration = models.DateTimeField(verbose_name='过期时间')


class Account(models.Model):
    accname = models.CharField(verbose_name='账户名',max_length=255)
    password = models.CharField(verbose_name='密码',max_length=255)
    identity = models.CharField(verbose_name='身份',max_length=255)
    email = models.EmailField(verbose_name='邮箱')
    birth = models.DateField(verbose_name='出生日期')
    sex = models.BooleanField(verbose_name='性别')
    teacher = models.ForeignKey(verbose_name='教师',to=Teacher,on_delete=models.CASCADE,null=True,blank=True)
    first = models.BooleanField(verbose_name='密码状态',default=0)


class Dictionary(models.Model):
    name = models.CharField(verbose_name='名',max_length=255)
    value = models.CharField(verbose_name='值',max_length=255)