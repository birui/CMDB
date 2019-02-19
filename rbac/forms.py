#coding=utf-8
from django.forms import ModelForm
from .models import UserInfo, Role, Permission, Menu


class UserInfoModelForm(ModelForm):
    class Meta:
        #关联表
        model = UserInfo
        #表单中使用所有字段
        fields = '__all__'
        #列表的值
        labels = {
            'username': '用户名',
            'password': '密码',
            'nickname': '昵称',
            'email': '邮箱',
            'roles': '角色',
        }


class RoleModelForm(ModelForm):
    class Meta:
        model = Role
        fields = '__all__'
        labels = {
            'title': '角色',
            'permissions': '权限',
        }


class PermissionModelForm(ModelForm):
    class Meta:
        model = Permission
        fields = '__all__'
        labels = {
            'title': '权限',
            'url': 'url',
            'menu': '所属菜单'
        }


class MenuModelForm(ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        labels = {
            'title': '菜单',
            'parent': '父级菜单',
        }
