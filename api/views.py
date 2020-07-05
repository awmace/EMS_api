from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin,UpdateModelMixin
# Create your views here.
from api.models import User, Employee
from api.serializers import UserModelSerializer, EmployeeSerializer
from utils.response import APIResponse


class UserAPIView(APIView):
    def post(self, request, *args, **kwargs):
        # 前端用户注册请求的处理
        data = request.data
        if data['password'] != data['passwords']:
            return APIResponse(201, False)
        serializer = UserModelSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()
        return APIResponse(200, True, results=UserModelSerializer(user_obj).data)

    def get(self, request, *args, **kwargs):
        # 前端用户登录请求的处理
        username = request.query_params.get('username')
        password = request.query_params.get('password')
        user = User.objects.filter(username=username, password=password).first()
        if user:
            data = UserModelSerializer(user).data
            return APIResponse(200, True, data)
        return APIResponse(400, False)


class EmployeeAPIView(GenericAPIView,
                      ListModelMixin,
                      CreateModelMixin,
                      DestroyModelMixin,
                      RetrieveModelMixin,
                      UpdateModelMixin):
    queryset = Employee.objects.all()  # 查询所有员工信息
    serializer_class = EmployeeSerializer
    lookup_field = "id"


    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            user=self.retrieve(request, *args, **kwargs)
            return APIResponse(200, True, results=user.data)
        else:
            user_list = self.list(request, *args, **kwargs)
            return APIResponse(200, True, results=user_list.data)

    def post(self, request, *args, **kwargs):
        # data = request.data
        # print(data)
        user = self.create(request, *args, **kwargs)
        return APIResponse(200, True, results=user.data)

    def delete(self, request, *args, **kwargs):
        id=kwargs.get('id')
        print(id)
        self.destroy(request, *args, **kwargs)
        return APIResponse(200, True, '删除成功')

    def put(self, request, *args, **kwargs):
        self.update(request, *args, **kwargs)
        return APIResponse(200, True, '修改成功')
