from django.db import models

# Create your models here.

class Teacher(models.Model):
    code = models.CharField(verbose_name='工号',max_length=255,unique=True)
    name = models.CharField(verbose_name='姓名',max_length=255)
    professional_rank = models.IntegerField(verbose_name='职称')
    phone = models.CharField(verbose_name='联系方式',max_length=255)
    academe = models.IntegerField(verbose_name='学院')
    faculty = models.IntegerField(verbose_name='系')
    education = models.IntegerField(verbose_name='学历')
    remark = models.CharField(verbose_name='备注',max_length=255)