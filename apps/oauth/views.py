from rest_framework.generics import GenericAPIView
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response

from rest_framework.views import APIView

from oauth.models import QQOauthUser
from oauth.serializers import OAuthQQUserSerializer
from oauth.utils import QQLoginTool
from users.models import User


class QQAuthorLoginView(APIView):
    """ 获取qq登录地址后返回code的视图 """
    def get(self, request):
        # 获取到next后面的参数，是一个code
        next = request.query_params.get('next')
        # 实例化qq工具对象
        oauth = QQLoginTool(state=next)
        # 得到登录地址
        login_url = oauth.get_login_code()

        return Response({'login_url': login_url})


class QQAuthUserView(GenericAPIView):
    """ qq登录用户数据 """
    # 制定一个序列化器，post方法专用
    serializer_class = OAuthQQUserSerializer

    def get(self, request):
        code = request.query_params.get('code')
        print(code)
        if not code:
            return Response({'message': 'code为空'})
        # 实例化qq工具
        oauth = QQLoginTool()
        access_token = oauth.get_access_token(code)    # 把code放进去，得到access_token
        openid = oauth.get_openid(access_token)        # 把access_token放进去，得到openid

        # 判断openid是否存在数据库
        try:
            qq_user = QQOauthUser.objects.get(openid=openid)
            print('我已经存在了，可以直接登录了')
            # 找到用户，生成token
            user = qq_user.user
            print('这个用户是：', user)
            # 加密一下数据，以token的形式返回
            jwt_payload = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload(user)
            token = jwt_encode(payload)
            # 返回的登录数据是user_id，username，token
            data = {
                'user_id': user.id,
                'username': user.username,
                'token': token
            }
            return Response(data)
        except QQOauthUser.DoesNotExist:
            print('openid是新的，代表这个用户是新绑定的用户')
            # openid是新的就直接返回token
            # TODO
            # 这里需要返回一个自定义的access_token数据，里面包含用户名
            # 其中，不能单独返回access_token，需要返回一个带有access_token键的数据
            token = oauth.generate_save_user_token(openid)
            return Response({'access_token': token})

    def post(self, request):
        """ 保存新绑定qq登录的用户 """
        data = request.data    # 得到前端传来的数据
        # 这个时候不能直接入库，需要放到序列化器中校验一下
        print('看看前端的数据是否包含了access_token', data)

        s = self.get_serializer(data=data)
        s.is_valid(raise_exception=True)
        user = s.save()
        # 保存数据之后，渲染token的登录数据
        jwt_payload = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload(user)
        token = jwt_encode(payload)
        # 前端需要的数据
        data = {
            'token': token,
            'user_id': user.id,
            'mobile': user.mobile
        }

        return Response(data)





