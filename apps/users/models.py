from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous.jws import TimedJSONWebSignatureSerializer as JWTSerializer, BadData

from utils.models import BaseModel


class User(AbstractUser):
    """ 用户模型类 """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True, on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_verify_mail_url(self, instance):
        """ 生成邮箱验证url """
        s = JWTSerializer(settings.SECRET_KEY, 3600*24*7)
        data = {'user_id': instance.id, 'email': instance.email}
        print(data)
        verify_url = s.dumps(data).decode()    # 加密数据
        print('加密后的邮箱url', verify_url)
        return verify_url

    @staticmethod
    def check_verify_mail_url(token):
        """ 解密邮箱链接 """
        s = JWTSerializer(settings.SECRET_KEY, 3600*24*7)
        try:
            data = s.loads(token)
            print('解密邮箱后：', data)
        except BadData as e:
            return None
        else:
            user_id = data['user_id']
            email = data['email']
            # 查询这个人的id和邮箱必须一致才能修改邮箱字段的状态
            try:
                user = User.objects.get(id=user_id, email=email)
            except User.DoesNotExist:
                return None
            else:
                return user


class Address(BaseModel):
    """
    用户地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses', verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses', verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']


