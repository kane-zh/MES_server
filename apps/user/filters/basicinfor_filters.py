from django_filters.rest_framework import  FilterSet
from django.contrib.auth.models import Group,Permission
from django.contrib.auth import get_user_model
from user.models import *

from Mes import settings
User= get_user_model()

class UserAuditRecordFilters(FilterSet):
    """
    操作记录
    """
    class Meta:
        model = UserAuditRecordModel
        fields=["uri"]

class PermissionInforFilters(FilterSet):
    """
    用户权限信息
    """
    class Meta:
        model = Permission
        fields=["codename"]

class GroupInforFilters(FilterSet):
    """
    用户组信息
    """
    class Meta:
        model = Group
        fields=["name"]

class UserInforFilters(FilterSet):
    """
    用户信息
    """
    class Meta:
        model = User
        fields=["post","username","auditor"]
