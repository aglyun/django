from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from oauth.models import OAuthQQUser
from oauth.serializers import OauthQQUserSerializer
from oauth.utils import QQAuthTool


class QQAuthURLView(APIView):
    """
    qq登录第一步的视图
    """
    def get(self, request):
        print('第一步骤已经被执行')
        next = request.query_params.get('next')
        oauth = QQAuthTool(state=next)
        login_url = oauth.get_qq_login_url()
        return Response({'login_url': login_url})


class QQAuthUserView(GenericAPIView):
    """
    创建qq用户视图
    """
    serializer_class = OauthQQUserSerializer

    def get(self, request):
        print('第二步骤已经被执行')
        code = request.query_params.get("code")
        if not code:
            return Response({'message': '缺少参数'}, status=status.HTTP_400_BAD_REQUEST)
        oauth = QQAuthTool()
        access_token = oauth.get_qq_access_token(code)    # 调用方法
        openid = oauth.get_qq_openid(access_token)        # 调用
        print('视图中的openid：', openid)
        # 上面的步骤已经完成了openid的获取，接下来是判断用户的绑定情况

        try:
            qq_openid = OAuthQQUser.objects.get(openid=openid)
            print('46行', qq_openid.openid)
        except OAuthQQUser.DoesNotExist as e:
            # 查询不到就返回自定义加密的access_token
            print('openid查询不到！！！')
            qq_access_token = oauth.generate_user_access_token(openid)   # 返回的是二进制类型的加密token
            return Response({'access_token': qq_access_token})
        else:
            print('这是存在openid的情况下触发的代码')
            user = qq_openid.user
            from rest_framework_jwt.settings import api_settings
            payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = payload_handler(user)
            token = encode_handler(payload)
            # 构造返回给前端的数据
            data = {
                'token': token,
                'user_id': user.id,
                'username': user.username,
            }

        return Response(data)

    def post(self, request):
        """ 保存qq登录用户的信息 """
        print('第三步开始执行')
        s = self.get_serializer(data=request.data)    # post用data，get用query_params
        print('第三部的前端数据：', request.data)
        s.is_valid(raise_exception=True)
        user = s.save()

        # 生成已登录的token

        return Response({'message': 'ok'})


