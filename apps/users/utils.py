# _*_coding:utf-8_*_
# 日期：2020/10/29  时间：上午10:12
# 加油！
import re

from django.contrib.auth.backends import ModelBackend

from users.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    自定义token登录返回的数据
    """
    data = {
        'token': token,
        'user_id': user.id,
        'username': user.username,
        'mobile': user.mobile,
    }
    return data


def get_user_by_account(account):
    """
    工具，根据账号获取user对象
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名获取手机号登录的认证
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user

