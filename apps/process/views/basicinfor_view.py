
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
from apps.process.serializes.basicinfor_serialize import *
from process.filters.basicinfor_filters import *
from apps.commonFunction import StandardResultsSetPagination,IsOwnerOrReadOnly

class ProcessAuditRecordView(ListModelMixin,RetrieveModelMixin, viewsets.GenericViewSet):
    """
    当前APP操作记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ProcessAuditRecordFilters
    search_fields = ["uri", "uri_id"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return ProcessAuditRecordSerialize_List
        elif self.action == "retrieve":
            return ProcessAuditRecordSerialize_Retrieve
        return ProcessAuditRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
            if self.request.user.is_superuser:     # 超级用户可以查看所有信息
                return ProcessAuditRecordModel.objects.all().order_by("-id")
            user = self.request.user.username
            condtions1 = {'user__iexact': user}     # 普通用户只能查看自己的信息
            if self.action == "list":  # 如果是查看列表
                if not self.request.user.has_perm('process.view_processauditrecordmodel'):  # 如果当前用户没有查看权限
                    raise exceptions.PermissionDenied
            if self.action == "retrieve":  # 如果是查看详情
                if not self.request.user.has_perm('process.read_processauditrecordmodel'):  # 如果当前用户没有查看详情权限
                    raise exceptions.PermissionDenied
            return ProcessAuditRecordModel.objects.filter(Q(**condtions1))

class ProcessAlterRecordView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP审核记录
    """
    queryset = ProcessAlterRecordModel.objects.all().order_by("-id")
    serializer_class = ProcessAlterRecordSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class ProcessImageView(CreateModelMixin,viewsets.GenericViewSet):
    """
     当前APP图片项
    """
    queryset = ProcessImageModel.objects.all().order_by("-id")
    serializer_class = ProcessImageSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class ProcessFileView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP文件项
    """
    queryset = ProcessFileModel.objects.all().order_by("-id")
    serializer_class = ProcessFileSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class UnitTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    计量单位类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = UnitTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return UnitTypeDefinitionSerialize_Create
        elif self.action == "list":
            return UnitTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return UnitTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return UnitTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return UnitTypeDefinitionSerialize_Partial
        return UnitTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return UnitTypeDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_unittypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_unittypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return UnitTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")



class UnitTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    计量单位类型层级结构
    """
    serializer_class = UnitTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('process.view_unittypedefinitionmodel')):
            return UnitTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied


class UnitInforDefinitionView(CreateModelMixin, ListModelMixin,
                        RetrieveModelMixin, UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    计量单位定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = UnitInforDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return UnitInforDefinitionSerialize_Create
        elif self.action == "list":
            return UnitInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return UnitInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return  UnitInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return UnitInforDefinitionSerialize_Partial
        return UnitInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return UnitInforDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_unitinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_unitinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return UnitInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")


class MaterialTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    物料类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = MaterialTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return MaterialTypeDefinitionSerialize_Create
        elif self.action == "list":
            return MaterialTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return MaterialTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return MaterialTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return MaterialTypeDefinitionSerialize_Partial
        return MaterialTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return MaterialTypeDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_materialtypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_materialtypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return MaterialTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")

class MaterialTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    物料类型层级结构
    """
    serializer_class = MaterialTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('process.view_materialtypedefinitionmodel')):
            return MaterialTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class MaterialInforDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    物料信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = MaterialInforDefinitionFilters
    search_fields = ["name","code","character"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return MaterialInforDefinitionSerialize_Create
        elif self.action == "list":
            return MaterialInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return MaterialInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return  MaterialInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return MaterialInforDefinitionSerialize_Partial
        return MaterialInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return MaterialInforDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_materialinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_materialinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return MaterialInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class SemifinishedTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    半成品类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = SemifinishedTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedTypeDefinitionSerialize_Create
        elif self.action == "list":
            return SemifinishedTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return SemifinishedTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return SemifinishedTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return SemifinishedTypeDefinitionSerialize_Partial
        return SemifinishedTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return SemifinishedTypeDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_semifinishedtypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_semifinishedtypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return SemifinishedTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")

class SemifinishedTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    半成品类型层级结构
    """
    serializer_class = SemifinishedTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('process.view_semifinishedtypedefinitionmodel')):
            return SemifinishedTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class SemifinishedInforDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    半成品信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = SemifinishedInforDefinitionFilters
    search_fields = ["name","code","routeType_code","routeType_name","route_code","route_name"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedInforDefinitionSerialize_Create
        elif self.action == "list":
            return SemifinishedInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return SemifinishedInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return SemifinishedInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return SemifinishedInforDefinitionSerialize_Partial
        return SemifinishedInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return SemifinishedInforDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_semifinishedinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_semifinishedinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return SemifinishedInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")

class ProductTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    产品类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductTypeDefinitionSerialize_Create
        elif self.action == "list":
            return ProductTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return ProductTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return ProductTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return ProductTypeDefinitionSerialize_Partial
        return ProductTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductTypeDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_producttypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_producttypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ProductTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")

class ProductTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    产品类型层级结构
    """
    serializer_class = ProductTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('process.view_producttypedefinitionmodel')):
            return ProductTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class ProductInforDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    产品信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductInforDefinitionFilters
    search_fields = ["name","code","routeType_code","routeType_name","route_code","route_name"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductInforDefinitionSerialize_Create
        elif self.action == "list":
            return ProductInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return ProductInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return ProductInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return ProductInforDefinitionSerialize_Partial
        return ProductInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductInforDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_productinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_productinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ProductInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")


class StationTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    工位类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = StationTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return StationTypeDefinitionSerialize_Create
        elif self.action == "list":
            return StationTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return StationTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return StationTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return StationTypeDefinitionSerialize_Partial
        return StationTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return StationTypeDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_stationtypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_stationtypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return StationTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")

class StationTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    工位类型层级结构
    """
    serializer_class = StationTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('process.view_stationtypedefinitionmodel')):
            return StationTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class StationMaterialView(CreateModelMixin,viewsets.GenericViewSet):
    """
    工位物料定义
    """
    queryset =  StationMaterialModel.objects.all()
    serializer_class  = StationMaterialSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class StationSemifinishedView(CreateModelMixin,viewsets.GenericViewSet):
    """
    工位半成品定义
    """
    queryset =  StationSemifinishedModel.objects.all()
    serializer_class  = StationSemifinishedSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class StationInforDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    工位定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = StationInforDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return StationInforDefinitionSerialize_Create
        elif self.action == "list":
            return StationInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return StationInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return  StationInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return StationInforDefinitionSerialize_Partial
        return StationInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return StationInforDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_stationinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_stationinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return StationInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")

class ProductRouteTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    生产线路类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductRouteTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductRouteTypeDefinitionSerialize_Create
        elif self.action == "list":
            return ProductRouteTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return ProductRouteTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return ProductRouteTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return ProductRouteTypeDefinitionSerialize_Partial
        return ProductRouteTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductRouteTypeDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_productroutetypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_productroutetypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ProductRouteTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")

class ProductRouteTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    生产线路类型层级结构
    """
    serializer_class = ProductRouteTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('process.view_productroutetypedefinitionmodel')):
            return ProductRouteTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied


class ProductRouteDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    生产路线定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductRouteDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductRouteDefinitionSerialize_Create
        elif self.action == "list":
            return ProductRouteDefinitionSerialize_List
        elif self.action == "retrieve":
            return ProductRouteDefinitionSerialize_Retrieve
        elif self.action == "update":
            return ProductRouteDefinitionSerialize_Update
        elif self.action == "partial_update":
            return ProductRouteDefinitionSerialize_Partial
        return ProductRouteDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductRouteDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_productroutedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_productroutedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ProductRouteDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class ProcessInforView( RetrieveModelMixin,viewsets.GenericViewSet):
    """
    工艺信息浏览
    """
    serializer_class  = ProcessInforSerialize
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated, ]



    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductRouteDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        condtions3 = {'state__in': ("使用中",)  # 其他用户 可以看到(使用中)的数据
                      }
        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('process.browse_productroutedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        return ProductRouteDefinitionModel.objects.filter(Q(**condtions3)).order_by("id")


class ProcessBoardView(CreateModelMixin, ListModelMixin,
                           RetrieveModelMixin, UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    工艺看板定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =ProcessBoardFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProcessBoardSerialize_Create
        elif self.action == "list":
            return ProcessBoardSerialize_List
        elif self.action == "retrieve":
            return ProcessBoardSerialize_Retrieve
        elif self.action == "update":
            return ProcessBoardSerialize_Update
        elif self.action == "partial_update":
            return ProcessBoardSerialize_Partial
        return ProcessBoardSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProcessBoardModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('process.view_processboardmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('process.read_processboardmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ProcessBoardModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("id")