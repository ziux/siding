from django.db import models
from course.models import TeachPlan
# Create your models here.

class Teacher(models.Model):
    createdate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedate = models.DateTimeField(auto_now=True, blank=True, null=True)
    df = models.BooleanField(default=False)
    code = models.CharField(verbose_name='工号',max_length=255,unique=True)
    name = models.CharField(verbose_name='姓名',max_length=255)
    professional_rank = models.CharField(verbose_name='职称',max_length=255)
    phone = models.CharField(verbose_name='联系方式',max_length=255)
    academe = models.CharField(verbose_name='学院', max_length=255)
    faculty = models.CharField(verbose_name='系', max_length=255)
    education = models.CharField(verbose_name='学历', max_length=255)
    remark = models.CharField(verbose_name='备注',max_length=255)


class PlanTeacher(models.Model):
    createdate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updatedate = models.DateTimeField(auto_now=True, blank=True, null=True)
    plan = models.ForeignKey(verbose_name='教学计划', to=TeachPlan, on_delete=models.CASCADE)
    teacher = models.ForeignKey(verbose_name='教师',to=Teacher,on_delete=models.CASCADE)
    type = models.CharField(verbose_name='教学方式',max_length=255)
    period = models.DecimalField(verbose_name='课程课时(h)', max_digits=4, decimal_places=1)
