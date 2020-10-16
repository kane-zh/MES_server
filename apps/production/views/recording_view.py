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
                                   DestroyModelMixin
                                   )
from apps.production.serializes.recording_serialize import *
from apps.production.filters.recording_filters import *
from apps.commonFunction import StandardResultsSetPagination



class AssessmentRecordView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    考核信息记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = AssessmentRecordFilters
    search_fields = ["handler",]
    ordering_fields = ["id","update_time","dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return AssessmentRecordSerialize_Create
        elif self.action == "list":
            return AssessmentRecordSerialize_List
        elif self.action == "retrieve":
            return AssessmentRecordSerialize_Retrieve
        elif self.action == "update":
            return AssessmentRecordSerialize_Update
        elif self.action == "partial_update":
            return AssessmentRecordSerialize_Partial
        return AssessmentRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return AssessmentRecordModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return AssessmentRecordModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('production.view_assessmentrecordmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('production.read_assessmentrecordmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return AssessmentRecordModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return AssessmentRecordModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class ProductDailyReportItemView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    产品生产日报子项信息定义
    """
    queryset = ProductDailyReportItemModel.objects.all().order_by("-id")
    serializer_class = ProductDailyReportItemSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class ProductDailyReportView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    产品生产日报信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductDailyReportFilters
    search_fields = ["name","code","workshop_code","workshop_name"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductDailyReportSerialize_Create
        elif self.action == "list":
            return ProductDailyReportSerialize_List
        elif self.action == "retrieve":
            return ProductDailyReportSerialize_Retrieve
        elif self.action == "update":
            return ProductDailyReportSerialize_Update
        elif self.action == "partial_update":
            return ProductDailyReportSerialize_Partial
        return ProductDailyReportSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return ProductDailyReportModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return ProductDailyReportModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('production.view_productdailyreportmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('production.read_productdailyreportmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return ProductDailyReportModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return ProductDailyReportModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class SemifinishedDailyReportItemView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    半成品生产日报子项信息定义
    """
    queryset = SemifinishedDailyReportItemModel.objects.all().order_by("-id")
    serializer_class = SemifinishedDailyReportItemSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class SemifinishedDailyReportView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    半成品生产日报信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = SemifinishedDailyReportFilters
    search_fields = ["name","code","workshop_code","workshop_name"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedDailyReportSerialize_Create
        elif self.action == "list":
            return SemifinishedDailyReportSerialize_List
        elif self.action == "retrieve":
            return SemifinishedDailyReportSerialize_Retrieve
        elif self.action == "update":
            return SemifinishedDailyReportSerialize_Update
        elif self.action == "partial_update":
            return SemifinishedDailyReportSerialize_Partial
        return SemifinishedDailyReportSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return SemifinishedDailyReportModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return SemifinishedDailyReportModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('production.view_semifinisheddailyreportmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('production.read_semifinisheddailyreportmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return SemifinishedDailyReportModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return SemifinishedDailyReportModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class ProductDataDefinitionView(CreateModelMixin, ListModelMixin,
                             DestroyModelMixin,RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    产品过程数据定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductdDataDefinitionFilters
    ordering_fields = ["id","update_time","dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductDataSerialize_Create
        elif self.action == "list":
            return ProductDataSerialize_List
        elif self.action == "retrieve":
            return ProductDataSerialize_Retrieve
        return ProductDataSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return ProductDataDefinitionModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return ProductDataDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user  # 信息创建者可以看到 (自己创建的)的数据,,
                      }
        condtions3 = { 'id__gt': 0       # 其他用户
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('production.view_productdatadefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('production.read_productdatadefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if start and stop:
            return ProductDataDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return ProductDataDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions3)).order_by(
                "-id")

class SemifinishedDataDefinitionView(CreateModelMixin, ListModelMixin,
                             DestroyModelMixin,RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    半成品过程数据定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = SemifinishedDataDefinitionFilters
    ordering_fields = ["id","update_time","dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedDataSerialize_Create
        elif self.action == "list":
            return SemifinishedDataSerialize_List
        elif self.action == "retrieve":
            return SemifinishedDataSerialize_Retrieve
        return SemifinishedDataSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return SemifinishedDataDefinitionModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return SemifinishedDataDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user  # 信息创建者可以看到 (自己创建的)的数据,,
                      }
        condtions3 = { 'id__gt': 0       # 其他用户
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('production.view_semifinisheddatadefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('production.read_semifinisheddatadefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if start and stop:
            return SemifinishedDataDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return SemifinishedDataDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions3)).order_by(
                "-id")
