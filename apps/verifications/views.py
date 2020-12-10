import random

from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms import tasks as sms_tasks
from tools.captcha.captcha import captcha
from tools.code_time import image_time, sms_time
from verifications.serializers import ImageCodeCheckSerialzier


class ImageCodeView(APIView):
    """ 图片验证码 """
    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()
        print('图片验证码是：', text)
        # 将验证码存入数据库
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex('img_%s' % image_code_id, image_time, text)
        return HttpResponse(image, content_type='image/jpg')


class SMSCodeView(GenericAPIView):
    """ 短信验证码 """
    # 指定一个图片验证码的校验序列化器
    serializer_class = ImageCodeCheckSerialzier

    def get(self, request, mobile):
        data = request.query_params     # 获取前端数据
        s = self.get_serializer(data=data)   # 将数据丢进序列化器中
        s.is_valid(raise_exception=True)
        # 验证通过后生成验证码
        sms_code = random.randint(100000, 999999)
        print('短信验证码是：', sms_code)
        # 存入redis数据库
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex('sms_%s' % mobile, sms_time, sms_code)

        # 发送验证码
        # send_sms_code(mobile, sms_code)
        # 异步发送短信
        # sms_tasks.send_sms_code.delay(mobile, sms_code)
        sms_tasks.send_sms_code.delay(mobile, sms_code)

        return Response({'message': 'OK'})
