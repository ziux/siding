from django.db import models
from course.models import TeachPlan


# Create your models here.
class TeachMaterialLib(models.Model):
    code = models.CharField(verbose_name='教材编号', unique=True, max_length=255)
    name = models.CharField(verbose_name='教材名称', max_length=255)
    price = models.DecimalField(verbose_name='价格', max_digits=6, decimal_places=2)
    type = models.IntegerField(verbose_name='教材类型')
    spec = models.CharField(verbose_name='教材规格')
    pubdate = models.DateField(verbose_name='出版时间')
    publisher = models.CharField(verbose_name='出版社', max_length=255)
    author = models.CharField(verbose_name='作者', max_length=255)
    remark = models.CharField(verbose_name='备注', max_length=255, null=True)


class PlanMaterial(models.Model):
    plan = models.ForeignKey(verbose_name='教学计划', to=TeachPlan, on_delete=models.CASCADE)
    material = models.ForeignKey(verbose_name='教材', to=TeachMaterialLib, on_delete=models.CASCADE)
    type = models.CharField(verbose_name='教材类型', max_length=255)
    main = models.BooleanField(verbose_name='是否为主教材')
