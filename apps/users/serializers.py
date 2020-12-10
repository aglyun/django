# _*_coding:utf-8_*_
# 日期：2020/10/28  时间：下午3:40
# 加油！
import re

from django.conf import settings
from django.core.mail import send_mail
from django_redis import get_redis_connection
from rest_framework import serializers

from users.models import User, Address
from rest_framework_jwt.settings import api_settings


class UserAddressSerializer(serializers.ModelSerializer):
    """ 用户地址序列化器 """
    # 省
    province = serializers.StringRelatedField(read_only=True)
    # 城市
    city = serializers.StringRelatedField(read_only=True)
    # 区
    district = serializers.StringRelatedField(read_only=True)
    # 省id
    province_id = serializers.IntegerField(label='省id', required=True)
    # 城市id
    city_id = serializers.IntegerField(label='城市id', required=True)
    # 区id
    district_id = serializers.IntegerField(label='区id', required=True)

    class Meta:
        # 指向地址数据模型
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def validate_mobile(self, value):
        """ 验证手机号码 """
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号码格式不正确')
        return value

    def create(self, validated_data):
        """ 保存数据 """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)



class EmailSerializer(serializers.ModelSerializer):
    """ 邮箱序列化器 """
    class Meta:
        # 指定用户模型表
        model = User
        # 显示id和邮箱
        fields = ('id', 'email')
        extra_kwargs = {
            'email': {
                # 设置邮箱必须是唯一的
                'required': True
            }
        }

    def update(self, instance, validated_data):
        """ 更新邮箱数据 """
        instance.email = validated_data['email']
        instance.save()

        u = User()
        # 调用加密的方法将邮箱数据加密，传入instance数据本身
        token = u.generate_verify_mail_url(instance)

        subject = '开源商城邮箱验证'
        to_email = '2166300075@qq.com'
        valid_url = 'http://demo.myuxi.wang/success_verify_email.html?token=%s' % token
        print(valid_url)
        html_message = '<p>欢迎使用开源商城!</p>' \
                       '<p>点我激活：</p>'\
                       '<p><a href="%s">%s</a></p>' % (valid_url, valid_url)
        # 发送邮件动作
        send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
        return instance


class UserInfoSerializer(serializers.ModelSerializer):
    """ 用户中心序列化器 """
    class Meta:
        model = User
        # 要显示的字段
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class CreateUserSerializer(serializers.ModelSerializer):
    """ 用户注册创建用户序列化器 """
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True, )
    allow = serializers.CharField(label='同意协议', write_only=True)
    token = serializers.CharField(label='登录状态的token', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password2', 'sms_code', 'allow', 'mobile', 'token']
        # 进一步约束字段
        extra_kwargs = {
            'username': {
                'max_length': 20,
                'min_length': 5,
                'error_messages': {
                    'max_length': '最大不能超过20个字符',
                    'min_length': '最小不能少于5个字符',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '最小不能少于5个字符',
                    'max_length': '最大不能少于20个字符',
                }
            }
        }

    def validate_mobile(self, value):
        """ 校验手机号码 """
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号码格式出错')
        return value

    def validate_allow(self, value):
        """ 检验用户是否同意协议 """
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, data):
        """ 判断密码 """
        if data['password'] != data['password2']:
            raise serializers.ValidationError('两次密码输入不正确')

        # 判断短信验证码
        redis_ok = get_redis_connection('verify_codes')
        mobile = data['mobile']    # 从数据中取到mobile
        db_sms_code = redis_ok.get('sms_%s' % mobile)
        if db_sms_code is None:
            raise serializers.ValidationError('无效的短信验证码')

        if data['sms_code'] != db_sms_code.decode():
            raise serializers.ValidationError('短信验证码错误')
        return data

    def create(self, validated_data):
        """
        创建用户
        """
        # 先删除不用存入数据库的数据
        del validated_data['password2']
        del validated_data['allow']
        del validated_data['sms_code']
        # 创建用户
        user = User.objects.create(**validated_data)
        # 调用认证系统的加密
        user.set_password(validated_data['password'])
        user.save()

        # 新增token生成方式
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        # 设置token
        user.token = token

        return user







