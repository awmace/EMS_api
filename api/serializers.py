from rest_framework import exceptions
from rest_framework.serializers import ModelSerializer

from api.models import User, Employee


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'username': {
                'required': True,
                'min_length': 3,
                'max_length': 8,
                'error_messages': {
                    'required': '用户名必填',
                    'min_length': '用户名不能低于3位字符',
                    'max_length': '密码不能多于8位字符',
                },
            },
            'password': {
                'required': True,
                'min_length': 6,
                'max_length': 16,
                'error_messages': {
                    'required': '密码不能为空',
                    'min_length': '密码不能低于6位字符',
                    'max_length': '密码不能多于16位字符',
                },
            },
            'tname': {
                'required': True,
                'min_length': 2,
                'max_length': 5,
                'error_messages': {
                    'required': '真实姓名不能为空',
                    'min_length': '不能低于2位字符',
                    'max_length': '不能多于5位字符',
                },
            }
        }

    def validate(self, attrs):
        username = attrs.get('username')
        user = User.objects.filter(username=username)
        if user:
            raise exceptions.ValidationError('用户名已存在')
        return attrs


class EmployeeSerializer(ModelSerializer):
    class Meta:
        model = Employee
        # fields = '__all__'
        fields = ('id', 'emp_name', 'img', 'salary', 'age', 'age_name')

        extra_kwargs = {
            'emp_name': {
                'required': True,
                'min_length': 2,
                'max_length': 5,
                'error_messages': {
                    'required': '员工名必填',
                    'min_length': '用户名不能低于2位字符',
                    'max_length': '密码不能多于5位字符',
                },
            },
        }

    def validate_age(self, value):
        if value > 55 & value < 18:
            raise exceptions.ValidationError("不在限定年龄范围内")
        return value
