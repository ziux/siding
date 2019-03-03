from django.db import models

# Create your models here.
class Token(models.Model):
    token = models.CharField(verbose_name='token', max_length=255, primary_key=True)
    value = models.BinaryField(verbose_name='值', max_length=2555, blank=True, null=True)
    expiration = models.DateTimeField(verbose_name='过期时间')