from django.db import models
from instructor.models import Teacher
from libs.delete_lib import delete_instance,delete_queryset
# Create your models here.
class Token(models.Model):
    token = models.CharField(verbose_name='token', max_length=255, primary_key=True)
    value = models.BinaryField(verbose_name='值', max_length=2555)
    expiration = models.DateTimeField(verbose_name='过期时间')


class Account(models.Model):
    createdate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedate = models.DateTimeField(auto_now=True, blank=True, null=True)
    accname = models.CharField(verbose_name='账户名',max_length=255)
    password = models.CharField(verbose_name='密码',max_length=255)
    identity = models.CharField(verbose_name='身份',max_length=255)
    email = models.EmailField(verbose_name='邮箱')
    birth = models.DateField(verbose_name='出生日期')
    lastlogin = models.DateTimeField(verbose_name='上次登录时间')
    sex = models.BooleanField(verbose_name='性别')
    teacher = models.ForeignKey(verbose_name='教师',to=Teacher,on_delete=models.CASCADE,null=True,blank=True)
    first = models.BooleanField(verbose_name='密码状态',default=0)


class Dictionary(models.Model):
    name = models.CharField(verbose_name='名',max_length=255)
    value = models.CharField(verbose_name='值',max_length=255)


# 操作日志表
class Operationlog(models.Model):
    createdate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedate = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey(to=Account, verbose_name='用户', on_delete=models.CASCADE)
    ip = models.CharField(max_length=255, verbose_name='登录IP')
    url = models.CharField(max_length=255, verbose_name='访问连接')
    level = models.CharField(verbose_name='日志级别')
    describe = models.CharField(max_length=255, verbose_name='描述')
    remark = models.CharField(max_length=255, verbose_name='备注', blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'operationlog'
