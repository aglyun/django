# _*_coding:utf-8_*_
# 日期：2020/10/14  时间：下午4:01
# 加油！
from django_redis import get_redis_connection
from redis import RedisError
from rest_framework import serializers


class ImageCodeCheckSerialzier(serializers.Serializer):
    """ 图片验证码序列化器 """
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(max_length=4, min_length=4)

    def validate(self, attrs):
        image_code_id = attrs['image_code_id']
        text = attrs['text']

        # 1. 从redis中查询图片验证码
        redis_conn = get_redis_connection('verify_codes')
        redis_text = redis_conn.get('img_%s' % image_code_id)
        print('得到redis中的验证码：', redis_text)
        # 2. 删除验证码
        if not redis_text:
            raise serializers.ValidationError('图片验证码无效')
        try:
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            print('删除错误：', e)
        # 3. 比较输入的验证码和reids的验证码
        redis_text = redis_text.decode()    # 解码
        if redis_text.lower() != text.lower():
            raise serializers.ValidationError('验证码错误(后台定义)')
        # 4. 判断是否在60秒内
        return attrs
