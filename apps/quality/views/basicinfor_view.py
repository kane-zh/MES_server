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
                                   UpdateModelMixin                        
                                   )
from apps.quality.serializes.basicinfor_serialize import *
from apps.quality.filters.basicinfor_filters import *
from apps.commonFunction import StandardResultsSetPagination,IsOwnerOrReadOnly

class QualityAuditRecordView(ListModelMixin,RetrieveModelMixin, viewsets.GenericViewSet):
    """
    当前APP操作记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = QualityAuditRecordFilters
    search_fields = ["uri", "uri_id"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return QualityAuditRecordSerialize_List
        elif self.action == "retrieve":
            return QualityAuditRecordSerialize_Retrieve
        return QualityAuditRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
            if self.request.user.is_superuser:     # 超级用户可以查看所有信息
                return QualityAuditRecordModel.objects.all().order_by("-id")
            user = self.request.user.username
            condtions1 = {'user__iexact': user}     # 普通用户只能查看自己的信息
            if self.action == "list":  # 如果是查看列表
                if not self.request.user.has_perm('quality.view_qualityauditrecordmodel'):  # 如果当前用户没有查看权限
                    raise exceptions.PermissionDenied
            if self.action == "retrieve":  # 如果是查看详情
                if not self.request.user.has_perm('quality.read_qualityauditrecordmodel'):  # 如果当前用户没有查看详情权限
                    raise exceptions.PermissionDenied
            return QualityAuditRecordModel.objects.filter(Q(**condtions1))

class QualityAlterRecordView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP审核记录
    """
    queryset = QualityAlterRecordModel.objects.all().order_by("-id")
    serializer_class = QualityAlterRecordSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class QualityImageView(CreateModelMixin,viewsets.GenericViewSet):
    """
     当前APP图片项
    """
    queryset = QualityImageModel.objects.all().order_by("-id")
    serializer_class = QualityImageSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class QualityFileView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP文件项
    """
    queryset = QualityFileModel.objects.all().order_by("-id")
    serializer_class = QualityFileSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]


class DefectTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    缺陷类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = DefectTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return DefectTypeDefinitionSerialize_Create
        elif self.action == "list":
            return DefectTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return DefectTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return DefectTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return DefectTypeDefinitionSerialize_Partial
        return DefectTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return DefectTypeDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('quality.view_defecttypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('quality.read_defecttypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return DefectTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class DefectTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    缺陷类型层级结构
    """
    serializer_class = DefectTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('quality.view_defecttypedefinitionmodel')):
            return DefectTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class DefectGradeDefinitionView(CreateModelMixin, ListModelMixin,
                        RetrieveModelMixin, UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    缺陷等级定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = DefectGradeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return DefectGradeDefinitionSerialize_Create
        elif self.action == "list":
            return DefectGradeDefinitionSerialize_List
        elif self.action == "retrieve":
            return DefectGradeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return  DefectGradeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return DefectGradeDefinitionSerialize_Partial
        return DefectGradeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return DefectGradeDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('quality.view_defectgradedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('quality.read_defectgradedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return DefectGradeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id") 


class DefectInforDefinitionView(CreateModelMixin, ListModelMixin,
                        RetrieveModelMixin, UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    缺陷定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = DefectInforDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return DefectInforDefinitionSerialize_Create
        elif self.action == "list":
            return DefectInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return DefectInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return  DefectInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return DefectInforDefinitionSerialize_Partial
        return DefectInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return DefectInforDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('quality.view_defectinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('quality.read_defectinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return DefectInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id") 


class InspectionStandardTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    检验标准类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = InspectionStandardTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return InspectionStandardTypeDefinitionSerialize_Create
        elif self.action == "list":
            return InspectionStandardTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return InspectionStandardTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return InspectionStandardTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return InspectionStandardTypeDefinitionSerialize_Partial
        return InspectionStandardTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return InspectionStandardTypeDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('quality.view_inspectionstandardtypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('quality.read_inspectionstandardtypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return InspectionStandardTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class InspectionStandardTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    检验标准类型层级结构
    """
    serializer_class = InspectionStandardTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('quality.view_inspectionstandardtypedefinitionmodel')):
            return InspectionStandardTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class InspectionStandardsDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    检验标准信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = InspectionStandardsDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return InspectionStandardsDefinitionSerialize_Create
        elif self.action == "list":
            return InspectionStandardsDefinitionSerialize_List
        elif self.action == "retrieve":
            return InspectionStandardsDefinitionSerialize_Retrieve
        elif self.action == "update":
            return  InspectionStandardsDefinitionSerialize_Update
        elif self.action == "partial_update":
            return InspectionStandardsDefinitionSerialize_Partial
        return InspectionStandardsDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return InspectionStandardDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('quality.view_inspectionstandardsdefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('quality.read_inspectionstandardsdefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return InspectionStandardDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class InspectionReportTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    检验汇报类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = InspectionReportTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time","samples_ration","ok_ration","ng_ration","concession_ration"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return InspectionReportTypeDefinitionSerialize_Create
        elif self.action == "list":
            return InspectionReportTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return InspectionReportTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return InspectionReportTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return InspectionReportTypeDefinitionSerialize_Partial
        return InspectionReportTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return InspectionReportTypeDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('quality.view_inspectionreporttypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('quality.read_inspectionreporttypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return InspectionReportTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class InspectionReportTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    检验汇报类型层级结构
    """
    serializer_class = InspectionReportTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('quality.view_inspectionreporttypedefinitionmodel')):
            return  InspectionReportTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class QualityBoardView(CreateModelMixin, ListModelMixin,
                           RetrieveModelMixin, UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    品质看板定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =QualityBoardFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return QualityBoardSerialize_Create
        elif self.action == "list":
            return QualityBoardSerialize_List
        elif self.action == "retrieve":
            return QualityBoardSerialize_Retrieve
        elif self.action == "update":
            return QualityBoardSerialize_Update
        elif self.action == "partial_update":
            return QualityBoardSerialize_Partial
        return QualityBoardSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return QualityBoardModel.objects.all().order_by("-id")   # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('quality.view_qualityboardmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('quality.read_qualityboardmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return QualityBoardModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")