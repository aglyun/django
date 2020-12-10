# _*_coding:utf-8_*_
# 日期：2020/10/29  时间：下午4:41
# 加油！
from django.db import models


class BaseModel(models.Model):
    """ 为模型类补充字段 """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True   # 表明这个是抽象模型类用于继承使用，数据库迁移的时候，不会生成表
