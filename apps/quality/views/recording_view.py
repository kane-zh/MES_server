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
from apps.quality.serializes.recording_serialize import *
from apps.quality.filters.recording_filters import *
from apps.commonFunction import StandardResultsSetPagination


class ReportInforItemDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    检验汇报子项信息定义
    """
    queryset = InspectionReportItemModel.objects.all().order_by("-id")
    serializer_class = ReportInforItemDefinitionSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class ReportInforDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    检验汇报信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ReportInforDefinitionFilters
    search_fields = ["name","code","result","handler"]
    ordering_fields = ["id","update_time","submit_sum","samples_sum","ok_sum","ng_sum","concession_sum","dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ReportInforDefinitionSerialize_Create
        elif self.action == "list":
            return ReportInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return ReportInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return ReportInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return ReportInforDefinitionSerialize_Partial
        return ReportInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return InspectionReportModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return InspectionReportModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('quality.view_reportinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('quality.read_reportinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return InspectionReportModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return InspectionReportModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

