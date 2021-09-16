from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class collect(models.Model):
    source_choice = (
        ('JD', '京东'),
        ('TEST', '测试数据'),
        ('OTHER', '其他'),
    )
    source = models.CharField(choices=source_choice, max_length=5, default='JD', verbose_name="数据来源")
    content = models.CharField(max_length=1000, verbose_name='内容')
    arthur = models.CharField(max_length=64,  verbose_name='作者')
    time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
    link = models.CharField(max_length=64, verbose_name="链接")

# class autoabstract(models.Model):
#     source = (
#         ('JD', '京东'),
#         ('DCD', '懂车帝'),
#         ('Auto', '汽车之家'),
#     )
#     content = models.CharField(unique=True, verbose_name='内容')
#     arthur = models.CharField(max_length=64, unique=True, verbose_name='作者')
#     time = models.DateTimeField(auto_now_add=True, verbose_name='时间')
#     link = models.DateField(null=True, blank=True, verbose_name="链接")