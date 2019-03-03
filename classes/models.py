from django.db import models

# Create your models here.

class Class(models.Model):
    code = models.CharField(verbose_name='班级编号',max_length=255,unique=True)
    name = models.CharField(verbose_name='班级名称',max_length=255)
    number = models.IntegerField(verbose_name='班级人数')
    session = models.IntegerField(verbose_name='届')
    academe = models.IntegerField(verbose_name='学院')
    faculty = models.IntegerField(verbose_name='系')
    remark = models.CharField(verbose_name='备注',max_length=255)