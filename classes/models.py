from django.db import models
from course.models import TeachPlan


# Create your models here.
# 班级表
class Class(models.Model):
    code = models.CharField(verbose_name='班级编号', max_length=255, unique=True)
    name = models.CharField(verbose_name='班级名称', max_length=255)
    number = models.IntegerField(verbose_name='班级人数')
    session = models.IntegerField(verbose_name='届')
    academe = models.CharField(verbose_name='学院', max_length=255)
    faculty = models.CharField(verbose_name='系', max_length=255)
    remark = models.CharField(verbose_name='备注', max_length=255)


# 计划班级对应表
class PlanClass(models.Model):
    plan = models.ForeignKey(verbose_name='教学计划', to=TeachPlan, on_delete=models.CASCADE)
    classes = models.ForeignKey(verbose_name='班级',to=Class,on_delete=models.CASCADE)
    number = models.IntegerField(verbose_name='上课人数')