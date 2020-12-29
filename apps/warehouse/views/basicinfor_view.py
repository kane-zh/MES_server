from rest_framework import viewsets
from rest_framework import  filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core import  exceptions
from django.db.models import Q
from rest_framework.mixins import (CreateModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin,
                                   UpdateModelMixin,                                   
                                   )
from apps.warehouse.serializes.basicinfor_serialize import *
from apps.warehouse.filters.basicinfor_filters import *
from apps.commonFunction import StandardResultsSetPagination ,IsOwnerOrReadOnly ,viewMiddleException


class WarehouseAuditRecordView(ListModelMixin,RetrieveModelMixin, viewsets.GenericViewSet):
    """
    当前APP操作记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = WarehouseAuditRecordFilters
    search_fields = ["uri", "uri_id"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return WarehouseAuditRecordSerialize_List
        elif self.action == "retrieve":
            return WarehouseAuditRecordSerialize_Retrieve
        return WarehouseAuditRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
            if self.request.user.is_superuser:     # 超级用户可以查看所有信息
                return WarehouseAuditRecordModel.objects.all().order_by("-id")
            user = self.request.user.username
            condtions1 = {'user__iexact': user}     # 普通用户只能查看自己的信息
            if self.action == "list":  # 如果是查看列表
                if not self.request.user.has_perm('warehouse.view_warehouseauditrecordmodel'):  # 如果当前用户没有查看权限
                    raise exceptions.PermissionDenied
            if self.action == "retrieve":  # 如果是查看详情
                if not self.request.user.has_perm('warehouse.read_warehouseauditrecordmodel'):  # 如果当前用户没有查看详情权限
                    raise exceptions.PermissionDenied
            return WarehouseAuditRecordModel.objects.filter(Q(**condtions1))

class WarehouseAlterRecordView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP审核记录
    """
    queryset = WarehouseAlterRecordModel.objects.all().order_by("-id")
    serializer_class = WarehouseAlterRecordSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class WarehouseImageView(CreateModelMixin,viewsets.GenericViewSet):
    """
     当前APP图片项
    """
    queryset = WarehouseImageModel.objects.all().order_by("-id")
    serializer_class = WarehouseImageSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class WarehouseFileView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP文件项
    """
    queryset = WarehouseFileModel.objects.all().order_by("-id")
    serializer_class = WarehouseFileSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class WarehouseDefinitionView(CreateModelMixin, ListModelMixin,
                              RetrieveModelMixin, UpdateModelMixin,
                              viewsets.GenericViewSet):
    """
    仓库信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = WarehouseDefinitionFilters
    search_fields = ["name","code","affiliation","location","principal"]
    ordering_fields = ["id","update_time","position_sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    #重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return WarehouseDefinitionSerialize_Create
        elif self.action == "list":
            return WarehouseDefinitionSerialize_List
        elif self.action == "retrieve":
            return WarehouseDefinitionSerialize_Retrieve
        elif self.action == "update":
            return  WarehouseDefinitionSerialize_Update
        elif self.action == "partial_update":
            return WarehouseDefinitionSerialize_Partial
        return WarehouseDefinitionSerialize_List

    # 重查询的方法，根据不同的操作查询不同的数据范围载数据
    def get_queryset(self):
        if self.request.user.is_superuser:
            return WarehouseDefinitionModel.objects.all().order_by("-id")   # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中",)  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中",)  # 所有用户 可以看到(使用中)的数据
                      }
        if self.action == "list":   # 如果是查看列表
             if  not self.request.user.has_perm('warehouse.view_warehousedefinitionmodel'):    # 如果当前用户没有查看权限
                 condtions3={}       #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":   # 如果是查看列表
             if  not self.request.user.has_perm('warehouse.read_warehousedefinitionmodel'):    # 如果当前用户没有查看详情权限
                 condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return WarehouseDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2)|Q(**condtions3))

class WarehouseDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    仓库层级结构
    """
    serializer_class = WarehouseDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('warehouse.view_warehousedefinitionmodel')):
            return WarehouseDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class PositionDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    仓位信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = PositionDefinitionFilters
    search_fields = ["name","code","place"]
    ordering_fields=["id","update_time","maximum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly ]
    permission_classes = [IsAuthenticated, ]

    #重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return PositionDefinitionSerialize_Create
        elif self.action == "list":
            return PositionDefinitionSerialize_List
        elif self.action == "retrieve":
            return PositionDefinitionSerialize_Retrieve
        elif self.action == "update":
            return PositionDefinitionSerialize_Update
        elif self.action == "partial_update":
            return PositionDefinitionSerialize_Partial
        return PositionDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return PositionDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中","闲置", "使用中")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中","闲置", "使用中",)  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","闲置")  # 其他用户 可以看到(使用中)的数据
                      }
        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.view_positiondefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_positiondefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return PositionDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id").order_by("-id")

class WarehouseBoardView(CreateModelMixin, ListModelMixin,
                           RetrieveModelMixin, UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    仓库看板定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =WarehouseBoardFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return WarehouseBoardSerialize_Create
        elif self.action == "list":
            return WarehouseBoardSerialize_List
        elif self.action == "retrieve":
            return WarehouseBoardSerialize_Retrieve
        elif self.action == "update":
            return WarehouseBoardSerialize_Update
        elif self.action == "partial_update":
            return WarehouseBoardSerialize_Partial
        return WarehouseBoardSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return WarehouseBoardModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('warehouse.view_warehouseboardmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_warehouseboardmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return WarehouseBoardModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")