# _*_coding:utf-8_*_
# 日期：2020/12/8  时间：下午12:07
# 加油！
from django.urls import re_path
from rest_framework.routers import DefaultRouter

from areas import views

urlpatterns = []
router = DefaultRouter()
router.register(r'areas', views.AreaViewSet, basename='areas')
urlpatterns += router.urls