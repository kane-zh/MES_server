from rest_framework import viewsets
from rest_framework import  filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   DestroyModelMixin
                                   )
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from apps.user.serializes.basicinfor_serialize import *
from apps.user.filters.basicinfor_filters import *
from apps.commonFunction import StandardResultsSetPagination ,IsOwnerOrReadOnly
from user.models import *
from django.contrib.auth.models import Group ,Permission
from django.core import  exceptions

class UserAuditRecordView(ListModelMixin,RetrieveModelMixin, viewsets.GenericViewSet):
    """
    操作日志
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = UserAuditRecordFilters
    search_fields = ["uri","uri_id"]
    ordering_fields = ["id"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    #重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return UserAuditRecordSerialize_List
        elif self.action == "retrieve":
            return UserAuditRecordSerialize_Retrieve
        return UserAuditRecordSerialize_List

    def get_queryset(self):
            if self.request.user.is_superuser:     # 超级用户可以查看所有信息
                return UserAuditRecordModel.objects.all().order_by("-id")
            user = self.request.user.username
            condtions1 = {'username__iexact': user}     # 普通用户只能查看自己的信息
            if self.action == "list":  # 如果是查看列表
                if not self.request.user.has_perm('user.view_userauditrecordmodel'):  # 如果当前用户没有查看权限
                    raise exceptions.PermissionDenied
            if self.action == "retrieve":  # 如果是查看详情
                if not self.request.user.has_perm('user.read_userauditrecordmodel'):  # 如果当前用户没有查看详情权限
                    raise exceptions.PermissionDenied
            return UserAuditRecordModel.objects.filter(Q(**condtions1))

class CustomBackend(ModelBackend):
    """
    自定义用户验证
    """
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username)|Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

class PermissionInforView(ListModelMixin,viewsets.GenericViewSet):
    """
    用户权限信息
    """
    serializer_class = PermissionInforSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =PermissionInforFilters
    search_fields = ["name"]
    ordering_fields = ["id"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

     # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Permission.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        if self.request.user.has_perm('user.admin_userinformodel'):  # 如果当前用户具有管理其他用户的权限
            return Permission.objects.all().order_by("-id")  # 授权用户可以查看所有权限信息
        else:
            raise exceptions.PermissionDenied  #非超级用户不能通过权限接口查看权限


class GroupInforView(CreateModelMixin, ListModelMixin,
                     DestroyModelMixin,viewsets.GenericViewSet):
    """
    用户组信息
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =GroupInforFilters
    search_fields = ["name"]
    ordering_fields = ["id"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return GroupInforSerialize_Create
        elif self.action == "list":
            return GroupInforSerialize_List
        return GroupInforSerialize_List

     # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Group.objects.all().order_by("-id") # 超级用户可以查看所有信息
        if self.request.user.has_perm('user.admin_userinformodel'):  # 如果当前用户具有管理其他用户的权限
            return Group.objects.all().order_by("-id")  # 授权用户可以查看所有组信息
        else:
            raise exceptions.PermissionDenied  #非超级用户不能通过用户组接口查看用户组信息


class UserInforView(CreateModelMixin, ListModelMixin,
                   RetrieveModelMixin, UpdateModelMixin,
                   viewsets.GenericViewSet):
    """
     用户信息视图
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =UserInforFilters
    search_fields = ["username","job_number"]
    ordering_fields = ["id"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return UserInforSerialize_Create
        elif self.action == "list":
            return UserInforSerialize_List
        elif self.action == "retrieve":
            return UserInforSerialize_Retrieve
        elif self.action == "update":
            return UserInforSerialize_Update
        elif self.action == "partial_update":
            return UserInforSerialize_Partial
        return UserInforSerialize_List

     # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
            if self.request.user.is_superuser:
                return User.objects.all().order_by("-id") # 超级用户可以查看所有信息
            if self.request.user.has_perm('user.admin_userinformodel'):  # 如果当前用户具有管理用户的权限
                return User.objects.all().order_by("-id")
            user = self.request.user.username
            condtions1 = {'username__iexact': user   # 当前登录账号
                          }
            condtions2 = {
                         'auditor__iexact': user    # 可被当前登录账号授权的账号
                          }
            condtions3 = {'username__iexact': user # 非当前登录用户
                          }
            if self.action == "list":  # 如果是查看列表
                if not self.request.user.has_perm('user.view_userinformodel'):  # 如果当前用户没有查看权限
                    condtions3 = {}  # 则不能查看非登录用户的信息（对于授权账号则被包含着condtions2中）
            if self.action == "retrieve":  # 如果是查看列表
                    condtions3 = {}  # 则不能查看非登录用户的信息（对于授权账号则被包含着condtions2中）
            if self.action == "update":  # 如果是更新列表
                    condtions3 = {}  # 则不能查看非登录用户的信息（对于授权账号则被包含着condtions2中）
            return User.objects.filter(Q(**condtions1) | Q(**condtions2) | ~Q(**condtions3))