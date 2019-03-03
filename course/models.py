from django.db import models


# Create your models here.
# 课程库
class CourseLib(models.Model):
    code = models.CharField(verbose_name='课程编号', max_length=255, unique=True)
    name = models.CharField(verbose_name='课程名称', max_length=255)
    describe = models.CharField(verbose_name='课程简述', max_length=255, null=True)
    type = models.CharField(verbose_name='课程类型', max_length=255)
    period = models.DecimalField(verbose_name='默认课时(h)', max_digits=4, decimal_places=1)
    remark = models.CharField(verbose_name='备注', null=True,max_length=255)


# 教学计划
class TeachPlan(models.Model):
    term = models.IntegerField(verbose_name='学期')
    course = models.ForeignKey(to=CourseLib, on_delete=models.CASCADE, verbose_name='课程')
    period = models.DecimalField(verbose_name='课程课时(h)', max_digits=4, decimal_places=1)
    number = models.IntegerField(verbose_name='上课总人数')
    remark = models.CharField(verbose_name='备注', max_length=255)
