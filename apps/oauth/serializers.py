# _*_coding:utf-8_*_
# 日期：2020/12/7  时间：下午9:12
# 加油！
from django_redis import get_redis_connection
from rest_framework import serializers

from oauth.models import QQOauthUser
from oauth.utils import QQLoginTool
from users.models import User


class OAuthQQUserSerializer(serializers.Serializer):
    """ 需要四个参数 """
    mobile = serializers.RegexField(label='手机号码', regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码', max_length=20, min_length=8)
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6)
    access_token = serializers.CharField(label='操作凭证')

    def validate(self, attrs):
        # 校验手机号码
        mobile = attrs['mobile']
        sms_code = attrs['sms_code']
        access_token = attrs['access_token']
        password = attrs['password']

        if not access_token:
            raise serializers.ValidationError('缺少access_token参数')

        # 调用解密方法取出openid
        oauth = QQLoginTool()
        openid = oauth.check_save_user_token(access_token)    # 取到openid
        attrs['openid'] = openid    # 新建一个key，用于保存至数据库

        # 校验短信验证码
        redis_conn = get_redis_connection('verify_codes')
        db_sms_code = redis_conn.get('sms_{}'.format(mobile))
        if sms_code != db_sms_code.decode():
            raise serializers.ValidationError('验证码错误')

        # 校验密码是否正确
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            pass
        else:
            if not user.check_password(password):
                # 判断：如果user没有已经加密的密码就报错
                raise serializers.ValidationError('密码错误！')
            # 新建一个新的键用来保存用户，方便下面的创建调用
            attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """ 当前面所有的校验通过后会执行这个函数 """
        user = validated_data.get('user')
        print(user)
        print(validated_data)
        mobile = validated_data['mobile']
        if not user:
            # 判断输入的用户(手机号码)不存在
            # 直接用手机号码创建用户
            user = User.objects.create_user(
                username=validated_data['mobile'],
                password=validated_data['password'],
                mobile=validated_data['mobile'],
            )
            print('用户使用的是新号码{}'.format(mobile))
        # 这个代码是号码已经存在后触发的事件，无论是新号码还是旧号码都会执行openid的绑定
        # 号码存在后直接添加openid的绑定即可
        print('用户使用的手机号码{}不是新号码'.format(mobile))
        QQOauthUser.objects.create(
            openid=validated_data['openid'],
            user=user
        )

        return user



