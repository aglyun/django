# _*_coding:utf-8_*_
# 日期：2020/12/2  时间：下午9:09
# 加油！
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
from django.conf import settings
from itsdangerous import TimedJSONWebSignatureSerializer as TimedJson, BadData


class QQLoginTool(object):
    """ qq登录工具"""
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        self.client_id = client_id or settings.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE

    def get_login_code(self):
        """ 获取登录地址的code """
        url = "https://graph.qq.com/oauth2.0/authorize?"
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state
        }
        url += urlencode(params)
        print('登录地址：', url)
        return url

    def get_access_token(self, code):
        """ 获取access_token """
        url = 'https://graph.qq.com/oauth2.0/token?'
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
        }
        url += urlencode(params)    # 拼接url
        res_data = urlopen(url).read().decode()
        # 通过qs将字符串转成字典
        dict_data = parse_qs(res_data)
        print('qs转换后:', dict_data)
        access_token = dict_data['access_token']
        print(access_token)
        return access_token

    def get_openid(self, access_token):
        """ 获取openid"""
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token[0]
        print(url)

        res_data = urlopen(url).read().decode()
        openid = res_data[45:-6]
        print('openid数据：', openid)
        return openid

    @staticmethod
    def generate_save_user_token(openid):
        """ 生成保存用户数据需要的token """
        # 使用itsdangerous模块下的TimedJSONWebSignatureSerializer进行保密和解密
        t = TimedJson(settings.SECRET_KEY, 300)
        # 构造自己的数据将他进行加密
        data = {
            'openid': openid,
        }
        # 生成的时候需要解码
        token = t.dumps(data).decode()
        return token

    @staticmethod
    def check_save_user_token(token):
        """ 用来上一步加密数据的解码 """
        t = TimedJson(settings.SECRET_KEY)    # 传入加密时的key
        try:
            data = t.loads(token)
            print('这是解密后的数据：', data)
        except BadData:
            # 如果解密失败会报BadData错误
            return None
        else:
            return data.get('openid')







