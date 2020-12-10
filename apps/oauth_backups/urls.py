# _*_coding:utf-8_*_
# 日期：2020/10/30  时间：上午9:08
# 加油！
from django.urls import re_path

from oauth import views

urlpatterns = [
    # /oauth/qq/authorization/  第一步：获取登录地址
    re_path(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
    # /oauth/qq/user/           第二步：获取access_token
    re_path(r'^qq/user/$', views.QQAuthUserView.as_view()),
    # /oauth/qq/user/           第三部，获取openid，保存并创建绑定用户

]