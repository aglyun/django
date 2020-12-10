# _*_coding:utf-8_*_
# 日期：2020/10/29  时间：下午3:46
# 加油！
import json
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
from itsdangerous import TimedJSONWebSignatureSerializer as JWTSerializer, BadData

from django.conf import settings


class QQAuthTool(object):
    """
    qq登录工具辅助
    """
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        self.client_id = client_id or settings.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE

    def get_qq_login_url(self):
        """ qq登录的url """
        url = 'https://graph.qq.com/oauth2.0/authorize?'
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
        }
        url += urlencode(params)
        return url

    def get_qq_access_token(self, code):
        """ qq返回access_token """
        url = 'https://graph.qq.com/oauth2.0/token?'
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'code': code,
        }
        # 进行编码
        url += urlencode(params)

        # 进行请求已经编码好的url
        response_data = urlopen(url).read()     # bytes
        response_data = response_data.decode()  # str

        response_dict = parse_qs(response_data)    # 把字符串转成字典
        # 将access_token取出来
        access_token = response_dict.get('access_token')
        print('qq工具中的：access_token', access_token)
        return access_token[0]

    def get_qq_openid(self, access_token):
        """ 获取qq登录后返回的openid"""
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token
        response_data = urlopen(url).read().decode()
        print('返回的数据：%s ，类型是：%s' % (response_data, type(response_data)))
        # 使用切取出openid
        # callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} );
        response_dict = response_data[10:-3]
        openid = json.loads(response_dict)
        openid = openid.get('openid')
        print('qq工具中的openid是：', openid)

        return openid

    def generate_user_access_token(self, openid):
        """ 生成加密后返回的access_token"""
        s = JWTSerializer(settings.SECRET_KEY, 600)
        data = {'openid': openid}
        access_token = s.dumps(data).decode()
        print('这个是qq工具中的access_token', access_token)
        return access_token

    def decode_user_access_token(self, access_token):
        """ 将生成的access_token 进行解密"""
        try:
            s = JWTSerializer(settings.SECRET_KEY, 600)
            data = s.loads(access_token)
        except BadData:
            return None
        else:
            return data.get('openid')




