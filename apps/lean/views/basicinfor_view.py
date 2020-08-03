from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import exceptions
from django.db.models import Q
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,
                                   )
from apps.lean.serializes.basicinfor_serialize import *
from apps.lean.filters.basicinfor_filters import *
from apps.commonFunction import StandardResultsSetPagination

class LeanAuditRecordView(ListModelMixin,RetrieveModelMixin, viewsets.GenericViewSet):
    """
    当前APP操作记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = LeanAuditRecordFilters
    search_fields = ["uri", "uri_id"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return LeanAuditRecordSerialize_List
        elif self.action == "retrieve":
            return LeanAuditRecordSerialize_Retrieve
        return LeanAuditRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
            if self.request.user.is_superuser:     # 超级用户可以查看所有信息
                return LeanAuditRecordModel.objects.all().order_by("-id")
            user = self.request.user.username
            condtions1 = {'user__iexact': user}     # 普通用户只能查看自己的信息
            if self.action == "list":  # 如果是查看列表
                if not self.request.user.has_perm('lean.view_leanauditrecordmodel'):  # 如果当前用户没有查看权限
                    raise exceptions.PermissionDenied
            if self.action == "retrieve":  # 如果是查看详情
                if not self.request.user.has_perm('lean.read_leanauditrecordmodel'):  # 如果当前用户没有查看详情权限
                    raise exceptions.PermissionDenied
            return LeanAuditRecordModel.objects.filter(Q(**condtions1))

class LeanAlterRecordView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP审核记录
    """
    queryset = LeanAlterRecordModel.objects.all().order_by("-id")
    serializer_class = LeanAlterRecordSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class LeanImageView(CreateModelMixin,viewsets.GenericViewSet):
    """
     当前APP图片项
    """
    queryset = LeanImageModel.objects.all().order_by("-id")
    serializer_class = LeanImageSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class LeanFileView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP文件项
    """
    queryset = LeanFileModel.objects.all().order_by("-id")
    serializer_class = LeanFileSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class LeanBoardView(CreateModelMixin, ListModelMixin,
                           RetrieveModelMixin, UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    精益看板定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =LeanBoardFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return LeanBoardSerialize_Create
        elif self.action == "list":
            return LeanBoardSerialize_List
        elif self.action == "retrieve":
            return LeanBoardSerialize_Retrieve
        elif self.action == "update":
            return LeanBoardSerialize_Update
        elif self.action == "partial_update":
            return LeanBoardSerialize_Partial
        return LeanBoardSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return LeanBoardModel.objects.all().oorder_by("-id")   # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中",)  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中",)  # 其他用户 可以看到(使用中)的数据
                      }
        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('lean.view_leanboardmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('lean.read_leanboardmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return LeanBoardModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).oorder_by("-id")