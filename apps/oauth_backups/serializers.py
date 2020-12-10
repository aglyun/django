# _*_coding:utf-8_*_
# 日期：2020/11/9  时间：下午3:37
# 加油！
from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.models import OAuthQQUser
from oauth.utils import QQAuthTool
from users.models import User


class OauthQQUserSerializer(serializers.Serializer):
    access_token = serializers.CharField(label='认证凭证', write_only=True)
    mobile = serializers.RegexField(label='手机号码', regex=r'^1[3-9]\d{9}$')
    sms_code = serializers.CharField(label='短信验证码')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)

    def validate(self, attrs):
        access_token = attrs['access_token']
        print('序列化器中的access_token: ', access_token)
        oauth = QQAuthTool()
        openid = oauth.decode_user_access_token(access_token)   # 得到解密后的openid
        print('序列化器中的openid：', openid)
        if not openid:
            raise serializers.ValidationError('access_token无效！')

        attrs['openid'] = openid    # 赋值

        sms_code = attrs['sms_code']    # 取出短信验证码
        mobile = attrs['mobile']        # 取出手机号码

        if not access_token:
            raise serializers.ValidationError('access_token无效！')
        # 从数据库中取出短信验证码
        redis_conn = get_redis_connection('verify_codes')
        redis_sms_code = redis_conn.get('sms_%s' % mobile)
        # 判断短信是否一致
        if sms_code != redis_sms_code.decode():
            raise serializers.ValidationError('验证码错误！')

        password = attrs['password']
        print('序列化器中的密码：', password)
        # 从数据库中查找用户
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            print('用户不存在，新账号')
            # attrs['user'] = mobile    # 创建一个用户，用户名是手机号
        else:
            # 如果用户存在了就检查密码是否一致
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误!!!')
            attrs['user'] = user
            print('53行看看user是什么？应该是fore3', user)
        return attrs

    def create(self, validated_data):
        return 'ok'








