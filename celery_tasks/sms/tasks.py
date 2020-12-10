# _*_coding:utf-8_*_
# 日期：2020/10/27  时间：下午8:37
# 加油！
import json
import uuid

from celery_tasks.sms.aliyunsms.sms_send import send_sms
from celery_tasks.main import app
import logging
logger = logging.getLogger('django')


@app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """发送短信验证码"""
    try:
        __business_id = uuid.uuid1()
        resu = send_sms(__business_id, mobile, "新奇特商城", "SMS_120410887", {"code":sms_code})
        result = json.loads(resu).get('Message')
    except Exception as e:
        logger.error("发送验证码短信[异常][ mobile: %s, message: %s ]" % (mobile, e))
    else:
        if result == "OK":
            logger.info("发送验证码短信[正常][ mobile: %s ]" % mobile)
        else:
            logger.warning("发送验证码短信[失败][ mobile: %s ]" % mobile)
