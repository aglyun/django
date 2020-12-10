# _*_coding:utf-8_*_
# 日期：2020/12/8  时间：下午4:53
# 加油！
from rest_framework import serializers

from areas.models import Area


class AreaSerializerSet(serializers.ModelSerializer):
    """ 行政区划信息序列化器 """
    class Meta:
        model = Area
        # 指定显示字段
        fields = ('id', 'name')


class SubAreaSerializerSet(serializers.ModelSerializer):
    """ 子行政区划信息序列化器 """
    subs = AreaSerializerSet(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')


