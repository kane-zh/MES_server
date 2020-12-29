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
from apps.plan.serializes.basicinfor_serialize import *
from apps.plan.filters.basicinfor_filters import *
from apps.commonFunction import StandardResultsSetPagination


class PlanAuditRecordView(ListModelMixin,RetrieveModelMixin, viewsets.GenericViewSet):
    """
    当前APP操作记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PlanAuditRecordFilters
    search_fields = ["uri", "uri_id"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return PlanAuditRecordSerialize_List
        elif self.action == "retrieve":
            return PlanAuditRecordSerialize_Retrieve
        return PlanAuditRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
            if self.request.user.is_superuser:     # 超级用户可以查看所有信息
                return PlanAuditRecordModel.objects.all().order_by("-id")
            user = self.request.user.username
            condtions1 = {'user__iexact': user}     # 普通用户只能查看自己的信息
            if self.action == "list":  # 如果是查看列表
                if not self.request.user.has_perm('plan.view_planauditrecordmodel'):  # 如果当前用户没有查看权限
                    raise exceptions.PermissionDenied
            if self.action == "retrieve":  # 如果是查看详情
                if not self.request.user.has_perm('plan.read_planauditrecordmodel'):  # 如果当前用户没有查看详情权限
                    raise exceptions.PermissionDenied
            return PlanAuditRecordModel.objects.filter(Q(**condtions1))

class PlanAlterRecordView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP审核记录
    """
    queryset = PlanAlterRecordModel.objects.all().order_by("-id")
    serializer_class = PlanAlterRecordSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class PlanImageView(CreateModelMixin,viewsets.GenericViewSet):
    """
     当前APP图片项
    """
    queryset = PlanImageModel.objects.all().order_by("-id")
    serializer_class = PlanImageSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class PlanFileView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP文件项
    """
    queryset = PlanFileModel.objects.all().order_by("-id")
    serializer_class = PlanFileSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]


class VendorTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    供应商类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = VendorTypeDefinitionFilters
    search_fields = ["name","code","company_name","company_abbre","qualification"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return VendorTypeDefinitionSerialize_Create
        elif self.action == "list":
            return VendorTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return VendorTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return VendorTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return VendorTypeDefinitionSerialize_Partial
        return VendorTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return VendorTypeDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('plan.view_vendortypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_vendortypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return VendorTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class VendorTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    供应商类型层级结构
    """
    serializer_class = VendorTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('plan.view_vendortypedefinitionmodel')):
            return VendorTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied


class VendorInforDefinitionView(CreateModelMixin, ListModelMixin,
                           RetrieveModelMixin, UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    供应商信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class= VendorInforDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    #重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return VendorInforDefinitionSerialize_Create
        elif self.action == "list":
            return VendorInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return VendorInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return VendorInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return VendorInforDefinitionSerialize_Partial
        return VendorInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return VendorInforDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('plan.view_vendorinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_vendorinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return VendorInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class ClientTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    客户类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ClientTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ClientTypeDefinitionSerialize_Create
        elif self.action == "list":
            return ClientTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return ClientTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return ClientTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return ClientTypeDefinitionSerialize_Partial
        return ClientTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ClientTypeDefinitionModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('plan.view_clienttypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_clienttypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ClientTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class ClientTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    客户类型层级结构
    """
    serializer_class = ClientTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('plan.view_clienttypedefinitionmodel')):
            return ClientTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class ClientInforDefinitionView(CreateModelMixin, ListModelMixin,
                           RetrieveModelMixin, UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    客户信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =ClientInforDefinitionFilters
    search_fields = ["name", "code", "company_name", "company_abbre",]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ClientInforDefinitionSerialize_Create
        elif self.action == "list":
            return ClientInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return ClientInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return ClientInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return ClientInforDefinitionSerialize_Partial
        return ClientInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ClientInforDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('plan.view_clientinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_clientinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ClientInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class SalesOrderItemCreateView(CreateModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    销售订单子项创建
    """
    queryset = SalesOrderItemCreateModel.objects.all().order_by("-id")
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly  ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SalesOrderItemCreateSerialize_Create
        elif self.action == "list":
            return SalesOrderItemCreateSerialize_List
        elif self.action == "partial_update":
            return SalesOrderItemCreateSerialize_Partial
        return SalesOrderItemCreateSerialize_List


class SalesOrderCreateView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    销售订单创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = SalesOrderCreateFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time","delivery_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SalesOrderCreateSerialize_Create
        elif self.action == "list":
            return SalesOrderCreateSerialize_List
        elif self.action == "retrieve":
            return SalesOrderCreateSerialize_Retrieve
        elif self.action == "update":
            return SalesOrderCreateSerialize_Update
        elif self.action == "partial_update":
            return SalesOrderCreateSerialize_Partial
        return SalesOrderCreateSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return SalesOrderCreateModel.objects.filter(delivery_time__gte=start).filter(delivery_time__lte=stop).order_by("-id")
            else:
                return SalesOrderCreateModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中","终止","完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中","终止","完成")  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","终止","完成")  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('plan.view_salesordercreatemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_salesordercreatemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if start and stop:
            return SalesOrderCreateModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                delivery_time__gte=start).filter(delivery_time__lte=stop).order_by("-id")
        else:
            return SalesOrderCreateModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")
class ProductTaskTypeView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    产品生产任务类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductTaskTypeFilters
    search_fields = ["name","code","company_name","company_abbre","qualification"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductTaskTypeSerialize_Create
        elif self.action == "list":
            return ProductTaskTypeSerialize_List
        elif self.action == "retrieve":
            return ProductTaskTypeSerialize_Retrieve
        elif self.action == "update":
            return ProductTaskTypeSerialize_Update
        elif self.action == "partial_update":
            return ProductTaskTypeSerialize_Partial
        return ProductTaskTypeSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductTaskTypeModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('plan.view_productTasktypemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_productTasktypemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ProductTaskTypeModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class ProductTaskTypeViews(ListModelMixin,viewsets.GenericViewSet):
    """
    产品生产任务类型层级结构
    """
    serializer_class = ProductTaskTypeSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('plan.view_productTasktypemodel')):
            return ProductTaskTypeModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied
class ProductTaskItemCreateView(CreateModelMixin, UpdateModelMixin,RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    产品生产任务子项创建
    """
    queryset = ProductTaskItemCreateModel.objects.all().order_by("-id")
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly  ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductTaskItemCreateSerialize_Create
        elif self.action == "retrieve":
            return ProductTaskItemCreateSerialize_Retrieve
        elif self.action == "partial_update":
            return ProductTaskItemCreateSerialize_Partial
        return ProductTaskItemCreateSerialize_List


class ProductTaskCreateView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    产品生产任务创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductTaskCreateFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time","delivery_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductTaskCreateSerialize_Create
        elif self.action == "list":
            return ProductTaskCreateSerialize_List
        elif self.action == "retrieve":
            return ProductTaskCreateSerialize_Retrieve
        elif self.action == "update":
            return ProductTaskCreateSerialize_Update
        elif self.action == "partial_update":
            return ProductTaskCreateSerialize_Partial
        return ProductTaskCreateSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return ProductTaskCreateModel.objects.filter(delivery_time__gte=start).filter(delivery_time__lte=stop).order_by("-id")
            else:
                return ProductTaskCreateModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中","挂起","终止","完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中","挂起","终止","完成")  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","挂起","终止","完成")  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('plan.view_producttaskcreatemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_producttaskcreatemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if start and stop:
            return ProductTaskCreateModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                delivery_time__gte=start).filter(delivery_time__lte=stop).order_by("-id")
        else:
            return ProductTaskCreateModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")
class SemifinishedTaskTypeView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    半成品生产任务类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = SemifinishedTaskTypeFilters
    search_fields = ["name","code","company_name","company_abbre","qualification"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedTaskTypeSerialize_Create
        elif self.action == "list":
            return SemifinishedTaskTypeSerialize_List
        elif self.action == "retrieve":
            return SemifinishedTaskTypeSerialize_Retrieve
        elif self.action == "update":
            return SemifinishedTaskTypeSerialize_Update
        elif self.action == "partial_update":
            return SemifinishedTaskTypeSerialize_Partial
        return SemifinishedTaskTypeSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return SemifinishedTaskTypeModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('plan.view_semifinishedTasktypemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_semifinishedTasktypemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return SemifinishedTaskTypeModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class SemifinishedTaskTypeViews(ListModelMixin,viewsets.GenericViewSet):
    """
    半成品生产任务类型层级结构
    """
    serializer_class = SemifinishedTaskTypeSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('plan.view_semifinishedTasktypemodel')):
            return SemifinishedTaskTypeModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied
class SemifinishedTaskItemCreateView(CreateModelMixin, UpdateModelMixin,RetrieveModelMixin,
                             viewsets.GenericViewSet):
    """
    半成品生产任务子项创建
    """
    queryset = SemifinishedTaskItemCreateModel.objects.all().order_by("-id")
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly  ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedTaskItemCreateSerialize_Create
        elif self.action == "retrieve":
            return SemifinishedTaskItemCreateSerialize_Retrieve
        elif self.action == "partial_update":
            return SemifinishedTaskItemCreateSerialize_Partial
        return SemifinishedTaskItemCreateSerialize_List


class SemifinishedTaskCreateView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    半成品生产任务创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = SemifinishedTaskCreateFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time","delivery_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedTaskCreateSerialize_Create
        elif self.action == "list":
            return SemifinishedTaskCreateSerialize_List
        elif self.action == "retrieve":
            return SemifinishedTaskCreateSerialize_Retrieve
        elif self.action == "update":
            return SemifinishedTaskCreateSerialize_Update
        elif self.action == "partial_update":
            return SemifinishedTaskCreateSerialize_Partial
        return SemifinishedTaskCreateSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return SemifinishedTaskCreateModel.objects.filter(delivery_time__gte=start).filter(delivery_time__lte=stop).order_by("-id")
            else:
                return SemifinishedTaskCreateModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中","挂起","终止","完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中","挂起","终止","完成")  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","挂起","终止","完成")  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('plan.view_semifinishedtaskcreatemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_semifinishedtaskcreatemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if start and stop:
            return SemifinishedTaskCreateModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                delivery_time__gte=start).filter(delivery_time__lte=stop).order_by("-id")
        else:
            return SemifinishedTaskCreateModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class PurchaseRequireItemCreateView(CreateModelMixin , viewsets.GenericViewSet):
    """
    采购需求单子相创建
    """

    queryset = PurchaseRequireItemCreateModel.objects.all().order_by("-id")
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly  ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return PurchaseRequireItemCreateSerialize_Create
        elif self.action == "list":
            return PurchaseRequireItemCreateSerialize_List
        elif self.action == "partial_update":
            return PurchaseRequireItemCreateSerialize_Partial
        return PurchaseRequireItemCreateSerialize_List

class PurchaseRequireCreateView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                           viewsets.GenericViewSet):
    """
    采购需求单创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = PurchaseRequireCreateFilters
    search_fields = ["name"]
    ordering_fields = ["id","update_time","dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return PurchaseRequireCreateSerialize_Create
        elif self.action == "list":
            return PurchaseRequireCreateSerialize_List
        elif self.action == "retrieve":
            return PurchaseRequireCreateSerialize_Retrieve
        elif self.action == "update":
            return PurchaseRequireCreateSerialize_Update
        elif self.action == "partial_update":
            return PurchaseRequireCreateSerialize_Partial
        return PurchaseRequireCreateSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return PurchaseRequireCreateModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return PurchaseRequireCreateModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中","挂起","终止","完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中","挂起","终止","完成")  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","挂起","终止","完成")  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('plan.view_purchaserequirecreatemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_purchaserequirecreatemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if start and stop:
            return PurchaseRequireCreateModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return PurchaseRequireCreateModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class MaterialManagePlanItemView(CreateModelMixin,UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    物料管理计划子项创建
    """
    queryset = MaterialManagePlanItemModel.objects.all().order_by("-id")
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly  ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return MaterialManagePlanSerialize_Create
        elif self.action == "list":
            return MaterialManagePlanSerialize_List
        elif self.action == "partial_update":
            return MaterialManagePlanSerialize_Partial
        return MaterialManagePlanSerialize_List

class MaterialManagePlanView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    物料管理计划创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = MaterialManagePlanFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time","dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]


    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return MaterialManagePlanSerialize_Create
        elif self.action == "list":
            return MaterialManagePlanSerialize_List
        elif self.action == "retrieve":
            return MaterialManagePlanSerialize_Retrieve
        elif self.action == "update":
            return MaterialManagePlanSerialize_Update
        elif self.action == "partial_update":
            return MaterialManagePlanSerialize_Partial
        return MaterialManagePlanSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return MaterialManagePlanModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return MaterialManagePlanModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中","挂起","终止","完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中","挂起","终止","完成")  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","挂起","终止","完成")  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('plan.view_materialmanageplanmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_materialmanageplanmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if start and stop:
            return MaterialManagePlanModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return MaterialManagePlanModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class SemifinishedManagePlanItemView(CreateModelMixin, UpdateModelMixin,
                                 viewsets.GenericViewSet):
    """
    半成品管理计划子项创建
    """
    queryset = SemifinishedManagePlanItemModel.objects.all().order_by("-id")
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedManagePlanSerialize_Create
        elif self.action == "list":
            return SemifinishedManagePlanSerialize_List
        elif self.action == "partial_update":
            return SemifinishedManagePlanSerialize_Partial
        return SemifinishedManagePlanSerialize_List


class SemifinishedManagePlanView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    半成品管理计划创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = SemifinishedManagePlanFilters
    search_fields = ["name", "code"]
    ordering_fields = ["id", "update_time", "dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedManagePlanSerialize_Create
        elif self.action == "list":
            return SemifinishedManagePlanSerialize_List
        elif self.action == "retrieve":
            return SemifinishedManagePlanSerialize_Retrieve
        elif self.action == "update":
            return SemifinishedManagePlanSerialize_Update
        elif self.action == "partial_update":
            return SemifinishedManagePlanSerialize_Partial
        return SemifinishedManagePlanSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return SemifinishedManagePlanModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return SemifinishedManagePlanModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中","挂起","终止","完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中","挂起","终止","完成")  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","挂起","终止","完成")  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('plan.view_semifinishedmanageplanmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  # 如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_semifinishedmanageplanmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  # 如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if start and stop:
            return SemifinishedManagePlanModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return SemifinishedManagePlanModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class ProductManagePlanItemView(CreateModelMixin, UpdateModelMixin,
                                 viewsets.GenericViewSet):
    """
    产品管理计划子项创建
    """
    queryset = ProductManagePlanItemModel.objects.all().order_by("-id")
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductManagePlanSerialize_Create
        elif self.action == "list":
            return ProductManagePlanSerialize_List
        elif self.action == "partial_update":
            return ProductManagePlanSerialize_Partial
        return ProductManagePlanSerialize_List


class ProductManagePlanView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    产品管理计划创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = ProductManagePlanFilters
    search_fields = ["name", "code"]
    ordering_fields = ["id", "update_time", "dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductManagePlanSerialize_Create
        elif self.action == "list":
            return ProductManagePlanSerialize_List
        elif self.action == "retrieve":
            return ProductManagePlanSerialize_Retrieve
        elif self.action == "update":
            return ProductManagePlanSerialize_Update
        elif self.action == "partial_update":
            return ProductManagePlanSerialize_Partial
        return ProductManagePlanSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return ProductManagePlanModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return ProductManagePlanModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中","挂起","终止","完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中","挂起","终止","完成")  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","挂起","终止","完成")  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('plan.view_productmanageplanmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  # 如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_productmanageplanmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  # 如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if start and stop:
            return ProductManagePlanModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return ProductManagePlanModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class EquipmentMaintainPlanItemView(CreateModelMixin,
                             viewsets.GenericViewSet):
    """
    设备维护计划子项创建
    """
    queryset = EquipmentMaintainPlanItemModel.objects.all().order_by("-id")
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,IsOwnerOrReadOnly  ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return EquipmentMaintainPlanItemSerialize_Create
        elif self.action == "list":
            return EquipmentMaintainPlanItemSerialize_List
        elif self.action == "partial_update":
            return EquipmentMaintainPlanItemSerialize_Partial
        return EquipmentMaintainPlanItemSerialize_List

class EquipmentMaintainPlanView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    设备维护计划创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = EquipmentMaintainPlanFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time","dataTime"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return EquipmentMaintainPlanSerialize_Create
        elif self.action == "list":
            return EquipmentMaintainPlanSerialize_List
        elif self.action == "retrieve":
            return EquipmentMaintainPlanSerialize_Retrieve
        elif self.action == "update":
            return EquipmentMaintainPlanSerialize_Update
        elif self.action == "partial_update":
            return EquipmentMaintainPlanSerialize_Partial
        return EquipmentMaintainPlanSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return EquipmentMaintainPlanModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return EquipmentMaintainPlanModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact': user,
                      'state__in': ("新建", "审核中", "使用中","挂起","终止","完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact': user,
                      'state__in': ("审核中", "使用中","挂起","终止","完成")  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in': ("使用中","挂起","终止","完成")  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list":  # 如果是查看列表
            if not self.request.user.has_perm('plan.view_equipmentmaintainplanmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_equipmentmaintainplanmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if start and stop:
            return EquipmentMaintainPlanModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return EquipmentMaintainPlanModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class PlanBoardView(CreateModelMixin, ListModelMixin,
                           RetrieveModelMixin, UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    计划看板定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =PlanBoardFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return PlanBoardSerialize_Create
        elif self.action == "list":
            return PlanBoardSerialize_List
        elif self.action == "retrieve":
            return PlanBoardSerialize_Retrieve
        elif self.action == "update":
            return PlanBoardSerialize_Update
        elif self.action == "partial_update":
            return PlanBoardSerialize_Partial
        return PlanBoardSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return PlanBoardModel.objects.all().order_by("-id")   # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('plan.view_planboardmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('plan.read_planboardmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return PlanBoardModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

