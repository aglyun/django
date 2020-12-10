# _*_coding:utf-8_*_
# 日期：2020/11/7  时间：下午3:46
# 加油！
from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.models import OAuthQQUser
from oauth.utils import QQAuthTool
from users.models import User


class OauthQQUserSerializer(serializers.Serializer):
    access_token = serializers.CharField(label='操作凭证', write_only=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码')

    class Meta:
        fields = ('id', 'token', 'username', 'access_token', 'mobile', 'password', 'sms_code')

    def validate(self, data):
        oauth = QQAuthTool()
        access_token = data['access_token']
        print('序列化器中的access_token', access_token)
        # 解密openid
        # openid = oauth.generate_user_access_token(access_token)
        openid = oauth.decode_user_access_token(access_token)
        print('得到解密后的openid', openid.get('openid'))
        print(type(openid))
        # 校验access_token
        if not openid:
            raise serializers.ValidationError('无效的access_token')

        data['openid'] = openid.get('openid')    # 赋值

        # 校验短信验证码
        sms_code = data['sms_code']
        mobile = data['mobile']
        redis_ok = get_redis_connection('verify_codes')
        real_sms_code = redis_ok.get('sms_%s' % mobile)    # 从数据库中取出验证码
        print(real_sms_code)
        if real_sms_code.decode() != sms_code:
            raise serializers.ValidationError('短信验证码错误')
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            print('用户不存在 新用户')
        else:
            password = data['password']
            if not user.check_password(password):    # 检查密码
                raise serializers.ValidationError('密码错误')
            data['user'] = user
        return data

    def create(self, validated_data):
        """ 创建用户 """
        # 移除数据表内没有的字段
        del validated_data['sms_code']
        user = validated_data['user']
        openid = validated_data['openid']
        mobile = validated_data['mobile']
        password = validated_data['password']

        # 如果用户不存在就创建用户
        if not user:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        # 添加qq绑定数据
        OAuthQQUser.objects.create(openid=openid, user=user)
        # 颁发登录令牌
        from rest_framework_jwt.settings import api_settings
        payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = payload_handler(user)
        token = encode_handler(payload)
        user.token = token

        return user




