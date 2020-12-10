# _*_coding:utf-8_*_
# 日期：2020/12/2  时间：下午9:01
# 加油！
from django.urls import re_path

from oauth import views

urlpatterns = [
    # 登录地址 oauth/qq/authorization/?next=/
    re_path('^qq/authorization/$', views.QQAuthorLoginView.as_view()),
    # 获取access_token  code oauth/qq/user/?code
    re_path('^qq/user/$', views.QQAuthUserView.as_view()),
    # /oauth/qq/user/
]