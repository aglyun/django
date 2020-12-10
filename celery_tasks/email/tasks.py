# _*_coding:utf-8_*_
# 日期：2020/11/25  时间：下午7:58
# 加油！


# 导入main首文件的app对象
from django.conf import settings
from django.core.mail import send_mail

from celery_tasks.main import app


def send_verify_email(to_email, verify_url):
    """
    发送邮箱验证码
    :param to_email: 收件人的邮箱
    :param verify_url: 验证的链接
    """

    subject = '开源商城邮箱验证'
    html_message = '<a href="%s">点我激活</a>' % verify_url

    # 发送邮件
    # send_mail(标题， 发件人， 收件人列表， 带有html代码的内容)
    send_mail(subject, '', settings.EMAIL_FROM, [to_email], html_message=html_message)
