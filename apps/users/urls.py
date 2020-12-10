# _*_coding:utf-8_*_
# 日期：2020/10/14  时间：下午3:12
# 加油！
from django.urls import re_path
from users import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    # 判断用户名 usernames/fore1/count/
    re_path(r'usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
    # 判断手机号码 /mobiles/17777556044/count/
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
    # 创建用户 /users/
    re_path(r'users/$', views.UserView.as_view()),
    # 登录用户
    re_path(r'authorizations/$', obtain_jwt_token),
    # 用户中心 /user/
    re_path(r'user', views.UserInfoView.as_view()),
    # 邮箱页面视图 /emails/
    re_path(r'^email/$', views.EmailView.as_view()),
    # 邮箱点击后验证 /emails/verification/
    re_path(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    # 用户添加地址
    re_path(r'^address/$')
]