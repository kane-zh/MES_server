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
from apps.equipment.serializes.basicinfor_serialize import *
from apps.equipment.filters.basicinfor_filters import *
from apps.commonFunction import StandardResultsSetPagination


class EquipmentAuditRecordView(ListModelMixin,RetrieveModelMixin, viewsets.GenericViewSet):
    """
    当前APP操作记录
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = EquipmentAuditRecordFilters
    search_fields = ["uri", "uri_id"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "list":
            return EquipmentAuditRecordSerialize_List
        elif self.action == "retrieve":
            return EquipmentAuditRecordSerialize_Retrieve
        return EquipmentAuditRecordSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
            if self.request.user.is_superuser:     # 超级用户可以查看所有信息
                return EquipmentAuditRecordModel.objects.all().order_by("-id")
            user = self.request.user.username
            condtions1 = {'user__iexact': user}     # 普通用户只能查看自己的信息
            if self.action == "list":  # 如果是查看列表
                if not self.request.user.has_perm('equipment.view_equipmentauditrecordmodel'):  # 如果当前用户没有查看权限
                    raise exceptions.PermissionDenied
            if self.action == "retrieve":  # 如果是查看详情
                if not self.request.user.has_perm('equipment.read_equipmentauditrecordmodel'):  # 如果当前用户没有查看详情权限
                    raise exceptions.PermissionDenied
            return EquipmentAuditRecordModel.objects.filter(Q(**condtions1))

class EquipmentAlterRecordView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP审核记录
    """
    queryset = EquipmentAlterRecordModel.objects.all().order_by("-id")
    serializer_class = EquipmentAlterRecordSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class EquipmentImageView(CreateModelMixin,viewsets.GenericViewSet):
    """
     当前APP图片项
    """
    queryset = EquipmentImageModel.objects.all().order_by("-id")
    serializer_class = EquipmentImageSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]

class EquipmentFileView(CreateModelMixin, viewsets.GenericViewSet):
    """
    当前APP文件项
    """
    queryset = EquipmentFileModel.objects.all().order_by("-id")
    serializer_class = EquipmentFileSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly]
    permission_classes = [IsAuthenticated, ]



class EquipmentVendorDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    设备厂商定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = EquipmentVendorDefinitionFilters
    search_fields = ["name","code","company_name","company_abbre"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return EquipmentVendorDefinitionSerialize_Create
        elif self.action == "list":
            return EquipmentVendorDefinitionSerialize_List
        elif self.action == "retrieve":
            return EquipmentVendorDefinitionSerialize_Retrieve
        elif self.action == "update":
            return EquipmentVendorDefinitionSerialize_Update
        elif self.action == "partial_update":
            return EquipmentVendorDefinitionSerialize_Partial
        return EquipmentVendorDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EquipmentVendorDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('equipment.view_equipmentvendordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_equipmentvendordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return EquipmentVendorDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class PartsTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    配件类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = PartsTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return PartsTypeDefinitionSerialize_Create
        elif self.action == "list":
            return PartsTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return PartsTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return PartsTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return PartsTypeDefinitionSerialize_Partial
        return PartsTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return PartsTypeDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('equipment.view_partstypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_partstypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return PartsTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class PartsTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    配件类型层级结构
    """
    serializer_class = PartsTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('equipment.view_partstypedefinitionmodel')):
            return  PartsTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class PartsInforDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    配件信息定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = PartsInforDefinitionFilters
    search_fields = ["name","code",]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return PartsInforDefinitionSerialize_Create
        elif self.action == "list":
            return PartsInforDefinitionSerialize_List
        elif self.action == "retrieve":
            return PartsInforDefinitionSerialize_Retrieve
        elif self.action == "update":
            return PartsInforDefinitionSerialize_Update
        elif self.action == "partial_update":
            return PartsInforDefinitionSerialize_Partial
        return PartsInforDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return PartsInforDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('equipment.view_partsinfordefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_partsinfordefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return PartsInforDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")


class EquipmentTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    设备类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = EquipmentTypeDefinitionFilters
    search_fields = ["name","code",]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return EquipmentTypeDefinitionSerialize_Create
        elif self.action == "list":
            return EquipmentTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return EquipmentTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return EquipmentTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return EquipmentTypeDefinitionSerialize_Partial
        return EquipmentTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EquipmentTypeDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('equipment.view_equipmenttypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_equipmenttypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return EquipmentTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class EquipmentTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    设备类型层级结构
    """
    serializer_class = EquipmentTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('equipment.view_equipmenttypedefinitionmodel')):
            return  EquipmentTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class EquipmentAccountView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    设备台账定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = EquipmentAccountFilters
    search_fields = ["name","code",]
    ordering_fields = ["id","update_time","dataOfActivation","dataOfPurchase"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return EquipmentAccountSerialize_Create
        elif self.action == "list":
            return EquipmentAccountSerialize_List
        elif self.action == "retrieve":
            return EquipmentAccountSerialize_Retrieve
        elif self.action == "update":
            return EquipmentAccountSerialize_Update
        elif self.action == "partial_update":
            return EquipmentAccountSerialize_Partial
        return EquipmentAccountSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EquipmentAccountModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('equipment.view_equipmentaccountmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_equipmentaccountmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return EquipmentAccountModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class MaintainRecordTypeDefinitionView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    维护记录类型定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = MaintainRecordTypeDefinitionFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return MaintainRecordTypeDefinitionSerialize_Create
        elif self.action == "list":
            return MaintainRecordTypeDefinitionSerialize_List
        elif self.action == "retrieve":
            return MaintainRecordTypeDefinitionSerialize_Retrieve
        elif self.action == "update":
            return MaintainRecordTypeDefinitionSerialize_Update
        elif self.action == "partial_update":
            return MaintainRecordTypeDefinitionSerialize_Partial
        return MaintainRecordTypeDefinitionSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return MaintainRecordTypeDefinitionModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('equipment.view_maintainrecordtypedefinitionmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_maintainrecordtypedefinitionmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return MaintainRecordTypeDefinitionModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class MaintainRecordTypeDefinitionViews(ListModelMixin,viewsets.GenericViewSet):
    """
    维护记录类型层级结构
    """
    serializer_class = MaintainRecordTypeDefinitionSerialize_First
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('equipment.view_maintainrecordtypedefinitionmodel')):
            return MaintainRecordTypeDefinitionModel.objects.filter(classes="一级类别")
        else:
            raise exceptions.PermissionDenied

class EquipmentBoardView(CreateModelMixin, ListModelMixin,
                           RetrieveModelMixin, UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    设备看板定义
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class =EquipmentBoardFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication,]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return EquipmentBoardSerialize_Create
        elif self.action == "list":
            return EquipmentBoardSerialize_List
        elif self.action == "retrieve":
            return EquipmentBoardSerialize_Retrieve
        elif self.action == "update":
            return EquipmentBoardSerialize_Update
        elif self.action == "partial_update":
            return EquipmentBoardSerialize_Partial
        return EquipmentBoardSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return EquipmentBoardModel.objects.all().order_by("-id")   # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('equipment.view_equipmentboardmodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('equipment.read_equipmentboardmodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return EquipmentBoardModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")