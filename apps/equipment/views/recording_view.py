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
from apps.equipment.serializes.recording_serialize import *
from apps.equipment.filters.recording_filters import *
from apps.commonFunction import StandardResultsSetPagination


class PartsUseRecordView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    配件消耗记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = PartsUseRecordFilters
    search_fields = ["name","code","handler",]
    ordering_fields = ["id","update_time","sum","dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return PartsUseRecordSerialize_Create
        elif self.action == "list":
            return PartsUseRecordSerialize_List
        elif self.action == "retrieve":
            return PartsUseRecordSerialize_Retrieve
        elif self.action == "update":
            return PartsUseRecordSerialize_Update
        elif self.action == "partial_update":
            return PartsUseRecordSerialize_Partial
        return PartsUseRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return PartsUseRecordModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return PartsUseRecordModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "完成",)  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("完成",)  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.view_partsuserecordmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_partsuserecordmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return PartsUseRecordModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return PartsUseRecordModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")


class MaintainRecordItemView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    维护记录子项信息定义
    """
    queryset = MaintainRecordItemModel.objects.all().order_by("-id")
    serializer_class = MaintainRecordItemSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class MaintainRecordView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    维护信息记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = MaintainRecordFilters
    search_fields = ["name","code","handler","result"]
    ordering_fields = ["id","update_time","dataTime","time_consuming"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return MaintainRecordSerialize_Create
        elif self.action == "list":
            return MaintainRecordSerialize_List
        elif self.action == "retrieve":
            return MaintainRecordSerialize_Retrieve
        elif self.action == "update":
            return MaintainRecordSerialize_Update
        elif self.action == "partial_update":
            return MaintainRecordSerialize_Partial
        return MaintainRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return MaintainRecordModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return MaintainRecordModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "完成",)  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("完成",)  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.view_maintainrecordmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_maintainrecordmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return MaintainRecordModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return MaintainRecordModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class EquipmentStateView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    设备状态信息
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = EquipmentStateFilters
    search_fields = ["name","code","task","handler"]
    ordering_fields=["id","update_time","runTime","allTime","sum","","",""]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return EquipmentStateSerialize_Create
        elif self.action == "list":
            return EquipmentStateSerialize_List
        elif self.action == "retrieve":
            return EquipmentStateSerialize_Retrieve
        elif self.action == "update":
            return EquipmentStateSerialize_Update
        elif self.action == "partial_update":
            return EquipmentStateSerialize_Partial
        return EquipmentStateSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EquipmentStateModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user
                      }
        condtions3 = {'id__gt': 0   # 其他用户
                      }
        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.view_equipmentstatemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_equipmentstatemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  # 如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "update":  # 如果是更新列表
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return EquipmentStateModel.objects.filter(Q(**condtions1) | Q(**condtions3)).order_by("-id")
    
