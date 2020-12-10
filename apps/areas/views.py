from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import RetrieveCacheResponseMixin

from areas.models import Area
from areas.serializers import AreaSerializerSet, SubAreaSerializerSet


class AreaViewSet(RetrieveCacheResponseMixin, ReadOnlyModelViewSet):
    """ 返回行政区划数据 """
    pagination_class = None

    def get_queryset(self):
        if self.action == 'list':
            # 如果action等于列表，就返回行政区划的数据
            return Area.objects.filter(parent=None)
        else:
            # 反之，返回所有数据
            return Area.objects.all()

    def get_serializer_class(self):
        """ 提供序列化器 """
        if self.action == 'list':
            return AreaSerializerSet
        else:
            return SubAreaSerializerSet
