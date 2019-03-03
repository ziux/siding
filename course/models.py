from django.db import models

# Create your models here.
class CourseLib(models.Model):
    code = models.CharField(verbose_name='课程编号',max_length=255,unique=True)
    name = models.CharField(verbose_name='课程名称',max_length=255)
    describe = models.CharField(verbose_name='课程简述',max_length=255,null=True)
    type = models.IntegerField(verbose_name='课程类型')
    period = models.DecimalField(verbose_name='默认课时(h)',max_digits=4,decimal_places=1)
    remark = models.CharField(verbose_name='备注',null=True)

