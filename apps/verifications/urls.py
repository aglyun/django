# _*_coding:utf-8_*_
# 日期：2020/10/14  时间：下午3:11
# 加油！
from django.urls import re_path

from verifications import views

urlpatterns =[
    # 图片验证码
    # image_codes/8ee5c9be-06ec-46e4-a130-f833891d8187/
    re_path('^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),

    # 短信验证码
    # sms_codes/17777556044/?text=rxsh&image_code_id=xxx
    re_path('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
]