# _*_coding:utf-8_*_
# 日期：2020/10/27  时间：下午8:35
# 加油！

from celery import Celery
import os

# 判断(这一步是否可有可无，这个是创建虚拟环境的)
if not os.getenv('django'):
    os.environ['django'] = 'mall_1014.settings'

# 创建应用
app = Celery('django')

# 导入配置
app.config_from_object('celery_tasks.config')

# 自动注册任务
app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email', ])