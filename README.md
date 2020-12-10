# 开源商城
***
#### apps: 应用文件夹
- areas 省份市区
- oauth qq登录
- users 用户注册登录
- verifications 图片和短信验证码
***
#### celery_tasks: 异步任务包
- email 异步发送邮箱
- sms 异步发送短信
***
#### tools: 第三方工具包
- aliyunsms 阿里云短信包
- captcha 生成图片验证码包
***
#### utils 工具包
***
#### script 脚本包
- import_areas_data_to_db.sh 执行该文件往数据库中添加省份地址信息
- sh import_areas_data_to_db.sh 执行，再按照提示输入mysql密码即可