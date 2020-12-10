# _*_coding:utf-8_*_
# 日期：2020/10/26  时间：下午2:58
# 加油！
from itsdangerous import TimedJSONWebSignatureSerializer as TimedJson
key = 'hbyuyan'
t = TimedJson(key, 600)
data = {
    'user': 'hbyuyan',
    'password': '123456'
}

token = t.dumps(data).decode()
print('加密后：', token)
token_data = t.loads(token)
print('解密后：', token_data)


tom = 'abc'
# print(f'我的名字是{s}')