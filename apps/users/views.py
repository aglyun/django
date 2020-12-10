from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.models import User
from rest_framework.permissions import IsAuthenticated
from users.serializers import CreateUserSerializer, UserInfoSerializer, EmailSerializer, UserAddressSerializer


class AddressViewSet(CreateModelMixin, UpdateModelMixin, GenericViewSet):
    """ 用户地址的新增和修改 """
    permission_classes = [IsAuthenticated]
    serializer_class = UserAddressSerializer



class EmailView(UpdateAPIView):
    """ 更新邮箱的视图 """
    # 设置权限认证
    permission_classes = [IsAuthenticated]
    serializer_class = EmailSerializer

    def get_object(self, *args, **kwargs):
        # 返回数据
        return self.request.user


class VerifyEmailView(APIView):
    """ 验证点击邮箱链接的视图 """
    def get(self, request):
        # 1. 获取token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token参数'}, status=status.HTTP_400_BAD_REQUEST)
        # 2. 验证token，调用解密url的方法，得到user或者None
        user = User.check_verify_mail_url(token)
        print('邮箱的user=', user)
        if user is None:
            return Response({'message': '链接信息无效'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 3. 验证通过后修改字段的默认值为True
            user.email_active = True
            # 4. 保存本次修改的操作
            user.save()
        return Response({'message': 'ok'})


class UserInfoView(RetrieveAPIView):
    """ 用户中心视图 """

    permission_classes = [IsAuthenticated]    # 权限认证
    serializer_class = UserInfoSerializer

    def get_object(self):
        # 返回前端需要的数据
        return self.request.user


class UsernameCountView(APIView):
    """
    用户名称数量
    """
    def get(self, request, username):
        print('用户名是：', username)
        count = User.objects.filter(username=username).count()
        print('用户名数量是：', count)
        data = {
            'username': username,
            'count': count
        }
        return Response(data)


class MobileCountView(APIView):
    """
    手机号数量
    """
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile': mobile,
            'count': count
        }
        return Response(data)


class UserView(CreateAPIView):
    """ 创建用户 """
    serializer_class = CreateUserSerializer
