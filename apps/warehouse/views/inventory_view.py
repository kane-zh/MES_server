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
from apps.warehouse.serializes.inventory_serialize import *
from apps.warehouse.filters.inventory_filters import *
from apps.commonFunction import StandardResultsSetPagination

class EquipmentStockDetailView(ListModelMixin, viewsets.GenericViewSet) :
    """
    设备库存明细
    """
    serializer_class = EquipmentStockDetailSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = EquipmentStockDetailFilters
    search_fields = ["position_name", "position_code","equipment_name", "equipment_code",]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self) :
        if (self.request.user.is_superuser) :
            return EquipmentStockDetailModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        elif (self.request.user.has_perm('warehouse.view_equipmentstockdetailmodel')) :
            return EquipmentStockDetailModel.objects.filter().order_by("-id")  # 超级用户可以查看所有信息
        else :
            raise exceptions.PermissionDenied

class PartsStockDetailView(ListModelMixin, viewsets.GenericViewSet) :
    """
    设备库存明细
    """
    serializer_class = PartsStockDetailSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PartsStockDetailFilters
    search_fields = ["position_name", "position_code","parts_name", "parts_code", ]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self) :
        if (self.request.user.is_superuser) :
            return PartsStockDetailModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        elif (self.request.user.has_perm('warehouse.view_partsstockdetailmodel')) :
            return PartsStockDetailModel.objects.filter().order_by("-id")  # 超级用户可以查看所有信息
        else :
            raise exceptions.PermissionDenied


class MaterialStockDetailView( ListModelMixin,viewsets.GenericViewSet):
    """
    物料库存明细
    """
    serializer_class = MaterialStockDetailSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class= MaterialStockDetailFilters
    search_fields=["position_name","position_code","material_name","material_code","batch"]
    ordering_fields=["id","update_time","sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser):
            return MaterialStockDetailModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
        elif (self.request.user.has_perm('warehouse.view_materialstockdetailmodel')):
            return MaterialStockDetailModel.objects.filter().order_by("-id")  # 超级用户可以查看所有信息
        else:
            raise exceptions.PermissionDenied

class SemifinishedStockDetailView( ListModelMixin,viewsets.GenericViewSet):
    """
    半成品库存明细
    """
    serializer_class = SemifinishedStockDetailSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class= SemifinishedStockDetailFilters
    search_fields = ["position_name", "position_code","semifinished_name", "semifinished_code", "batch"]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser):
            return SemifinishedStockDetailModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        elif (self.request.user.has_perm('warehouse.view_semifinishedstockdetailmodel')):
            return SemifinishedStockDetailModel.objects.filter().order_by("-id")  # 超级用户可以查看所有信息
        else:
            raise exceptions.PermissionDenied

class ProductStockDetailView( ListModelMixin,viewsets.GenericViewSet):
    """
    产品库存明细
    """
    serializer_class = ProductStockDetailSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class= ProductStockDetailFilters
    search_fields = ["position_name", "position_code","product_name", "product_code", "batch"]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser):
            return ProductStockDetailModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        elif (self.request.user.has_perm('warehouse.view_productstockdetailmodel')):
            return ProductStockDetailModel.objects.filter().order_by("-id")  # 超级用户可以查看所有信息
        else:
            raise exceptions.PermissionDenied
class EquipmentStockInforView(ListModelMixin, viewsets.GenericViewSet) :
    """
    设备库存信息
    """
    serializer_class = EquipmentStockInforSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = EquipmentStockInforFilters
    search_fields = ["equipment_name","equipment_code", ]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self) :
        if (self.request.user.is_superuser or self.request.user.has_perm('warehouse.view_equipmentstockinformodel')) :
            return EquipmentStockInforModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        else :
            raise exceptions.PermissionDenied

class PartsStockInforView(ListModelMixin, viewsets.GenericViewSet) :
    """
    设备库存信息
    """
    serializer_class = PartsStockInforSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PartsStockInforFilters
    search_fields = ["parts_name","parts_code",]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self) :
        if (self.request.user.is_superuser or self.request.user.has_perm('warehouse.view_partsstockinformodel')) :
            return PartsStockInforModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        else :
            raise exceptions.PermissionDenied

class MaterialStockInforView( ListModelMixin,viewsets.GenericViewSet):
    """
    物料库存信息
    """
    serializer_class = MaterialStockInforSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class= MaterialStockInforFilters
    search_fields = ["material_name", "material_code", "batch"]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('warehouse.view_materialstockinformodel')):
            return MaterialStockInforModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        else:
            raise exceptions.PermissionDenied

class SemifinishedStockInforView( ListModelMixin,viewsets.GenericViewSet):
    """
    半成品库存信息
    """
    serializer_class = SemifinishedStockInforSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class= SemifinishedStockInforFilters
    search_fields = ["semifinished_name","semifinished_code", "batch"]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('warehouse.view_semifinishedstockinformodel')):
            return SemifinishedStockInforModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        else:
            raise exceptions.PermissionDenied

class ProductStockInforView( ListModelMixin,viewsets.GenericViewSet):
    """
    产品库存信息
    """
    serializer_class = ProductStockInforSerialize_List
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class= ProductStockInforFilters
    search_fields = ["product_name","product_code", "batch"]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        if (self.request.user.is_superuser or self.request.user.has_perm('warehouse.view_productstockinformodel')):
            return ProductStockInforModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        else:
            raise exceptions.PermissionDenied
class EquipmentManageView(CreateModelMixin, ListModelMixin,
                         RetrieveModelMixin, UpdateModelMixin,
                         viewsets.GenericViewSet) :
    """
    设备管理
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = EquipmentManageFilters
    search_fields = ["position_name", "position_code","equipment_name", "equipment_code", "batch", "handler", ]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self) :
        if self.action == "create" :
            return EquipmentManageSerialize_Create
        elif self.action == "list" :
            return EquipmentManageSerialize_List
        elif self.action == "retrieve" :
            return EquipmentManageSerialize_Retrieve
        elif self.action == "update" :
            return EquipmentManageSerialize_Update
        elif self.action == "partial_update" :
            return EquipmentManageSerialize_Partial
        return EquipmentManageSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self) :
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return EquipmentManageModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return EquipmentManageModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact' : user,
                      'state__in' : ("新建", "审核中", "完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact' : user,
                      'state__in' : ("审核中", "完成",)  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in' : ("完成",)  # 其他用户 可以看到(使用中)的数据
                      }
        condtions4={}
        if self.action == "list" :  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.view_equipmentmanagemodel') :  # 如果当前用户没有查看权限
                condtions3 = {}  # 如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve" :  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_equipmentmanagemodel') :  # 如果当前用户没有查看详情权限
                condtions3 = {}  # 如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update" :  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update" :  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return EquipmentManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return EquipmentManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class PartsManageView(CreateModelMixin, ListModelMixin,
                         RetrieveModelMixin, UpdateModelMixin,
                         viewsets.GenericViewSet) :
    """
    备品管理
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = PartsManageFilters
    search_fields = ["position_name", "position_code", "parts_name", "parts_code", "handler", ]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self) :
        if self.action == "create" :
            return PartsManageSerialize_Create
        elif self.action == "list" :
            return PartsManageSerialize_List
        elif self.action == "retrieve" :
            return PartsManageSerialize_Retrieve
        elif self.action == "update" :
            return PartsManageSerialize_Update
        elif self.action == "partial_update" :
            return PartsManageSerialize_Partial
        return PartsManageSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self) :
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return PartsManageModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return PartsManageModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
        user = self.request.user.username
        condtions1 = {'create_user__iexact' : user,
                      'state__in' : ("新建", "审核中", "完成")  # 信息创建者可以看到 (新建,审核,使用中)的数据,,
                      }
        condtions2 = {'auditor__iexact' : user,
                      'state__in' : ("审核中", "完成",)  # 信息审核者可以看到 (审核,使用中)的数据
                      }
        condtions3 = {'state__in' : ("完成",)  # 其他用户 可以看到(使用中)的数据
                      }

        if self.action == "list" :  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.view_partsmanagemodel') :  # 如果当前用户没有查看权限
                condtions3 = {}  # 如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve" :  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_partsmanagemodel') :  # 如果当前用户没有查看详情权限
                condtions3 = {}  # 如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update" :  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update" :  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return PartsManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return PartsManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class MaterialManageView(CreateModelMixin, ListModelMixin,
                         RetrieveModelMixin,UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    物料管理
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class=MaterialManageFilters
    search_fields=["position_name","position_code","material_name","material_code","batch","handler",]
    ordering_fields=["id","update_time","sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return MaterialManageSerialize_Create
        elif self.action == "list":
            return MaterialManageSerialize_List
        elif self.action == "retrieve":
            return MaterialManageSerialize_Retrieve
        elif self.action == "update":
            return MaterialManageSerialize_Update
        elif self.action == "partial_update":
            return MaterialManageSerialize_Partial
        return MaterialManageSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return MaterialManageModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return MaterialManageModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('warehouse.view_materialmanagemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_materialmanagemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return MaterialManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return MaterialManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class SemifinishedManageView(CreateModelMixin, ListModelMixin,
                         RetrieveModelMixin,UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    半成品管理
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class=SemifinishedManageFilters
    search_fields = ["position_name", "position_code", "semifinished_name", "semifinished_code", "batch","handler",]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedManageSerialize_Create
        elif self.action == "list":
            return SemifinishedManageSerialize_List
        elif self.action == "retrieve":
            return SemifinishedManageSerialize_Retrieve
        elif self.action == "update":
            return SemifinishedManageSerialize_Update
        elif self.action == "partial_update":
            return SemifinishedManageSerialize_Partial
        return SemifinishedManageSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return SemifinishedManageModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return SemifinishedManageModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('warehouse.view_semifinishedmanagemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_semifinishedmanagemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return SemifinishedManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return SemifinishedManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class ProductManageView(CreateModelMixin, ListModelMixin,
                         RetrieveModelMixin,UpdateModelMixin,
                          viewsets.GenericViewSet):
    """
    产品管理
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class=ProductManageFilters
    search_fields = ["position_name", "position_code","product_name", "product_code", "batch","handler"]
    ordering_fields = ["id", "update_time", "sum"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductManageSerialize_Create
        elif self.action == "list":
            return ProductManageSerialize_List
        elif self.action == "retrieve":
            return ProductManageSerialize_Retrieve
        elif self.action == "update":
            return ProductManageSerialize_Update
        elif self.action == "partial_update":
            return ProductManageSerialize_Partial
        return ProductManageSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        start = self.request.query_params.get('start_time', None)
        stop = self.request.query_params.get('stop_time', None)
        if self.request.user.is_superuser:
            if start and stop:
                return ProductManageModel.objects.filter(dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
            else:
                return ProductManageModel.objects.all().order_by("-id")  # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('warehouse.view_productmanagemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_productmanagemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {}  #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        if start and stop:
            return ProductManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).filter(
                dataTime__gte=start).filter(dataTime__lte=stop).order_by("-id")
        else:
            return ProductManageModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by(
                "-id")

class MaterialWaringRuleItemView(CreateModelMixin, viewsets.GenericViewSet):
    """
    物料预警规则子项创建
    """
    queryset = MaterialWaringRuleItemModel.objects.all().order_by("-id")
    serializer_class = MaterialWaringRuleItemSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly ]
    permission_classes = [IsAuthenticated, ]


class MaterialWaringRuleView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    物料预警规则创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = MaterialWaringRuleFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return MaterialWaringRuleSerialize_Create
        elif self.action == "list":
            return MaterialWaringRuleSerialize_List
        elif self.action == "retrieve":
            return MaterialWaringRuleSerialize_Retrieve
        elif self.action == "update":
            return MaterialWaringRuleSerialize_Update
        elif self.action == "partial_update":
            return MaterialWaringRuleSerialize_Partial
        return MaterialWaringRuleSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return MaterialWaringRuleModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('warehouse.view_materialwaringrulemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_materialwaringrulemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return MaterialWaringRuleModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class SemifinishedWaringRuleItemView(CreateModelMixin, viewsets.GenericViewSet):
    """
    半成品预警规则子项创建
    """
    queryset = SemifinishedWaringRuleItemModel.objects.all().order_by("-id")
    serializer_class = SemifinishedWaringRuleItemSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly ]
    permission_classes = [IsAuthenticated, ]


class SemifinishedWaringRuleView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    半成品预警规则创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = SemifinishedWaringRuleFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return SemifinishedWaringRuleSerialize_Create
        elif self.action == "list":
            return SemifinishedWaringRuleSerialize_List
        elif self.action == "retrieve":
            return SemifinishedWaringRuleSerialize_Retrieve
        elif self.action == "update":
            return SemifinishedWaringRuleSerialize_Update
        elif self.action == "partial_update":
            return SemifinishedWaringRuleSerialize_Partial
        return SemifinishedWaringRuleSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return SemifinishedWaringRuleModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('warehouse.view_semifinishedwaringrulemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_semifinishedwaringrulemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return SemifinishedWaringRuleModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

class ProductWaringRuleItemView(CreateModelMixin, viewsets.GenericViewSet):
    """
    产品预警规则子项创建
    """
    queryset = ProductWaringRuleItemModel.objects.all().order_by("-id")
    serializer_class = ProductWaringRuleItemSerialize_Create
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, IsOwnerOrReadOnly ]
    permission_classes = [IsAuthenticated, ]

class ProductWaringRuleView(CreateModelMixin, ListModelMixin,
                             RetrieveModelMixin, UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    产品预警规则创建
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter)
    filter_class = ProductWaringRuleFilters
    search_fields = ["name","code"]
    ordering_fields = ["id","update_time"]
    authentication_classes = [SessionAuthentication, JSONWebTokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    # 重载获取序列化类的方法，根据不同的操作返回不同的序列化类
    def get_serializer_class(self):
        if self.action == "create":
            return ProductWaringRuleSerialize_Create
        elif self.action == "list":
            return ProductWaringRuleSerialize_List
        elif self.action == "retrieve":
            return ProductWaringRuleSerialize_Retrieve
        elif self.action == "update":
            return ProductWaringRuleSerialize_Update
        elif self.action == "partial_update":
            return ProductWaringRuleSerialize_Partial
        return ProductWaringRuleSerialize_List

    # 重载数据查询的方法，根据不同的操作查询不同的数据范围
    def get_queryset(self):
        if self.request.user.is_superuser:
            return ProductWaringRuleModel.objects.all().order_by("-id") # 超级用户可以查看所有信息
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
            if not self.request.user.has_perm('warehouse.view_productwaringrulemodel'):  # 如果当前用户没有查看权限
                condtions3 = {}  #如果普通用户不具备查看列表权限权限,则不能查看列表信息
        if self.action == "retrieve":  # 如果是查看列表
            if not self.request.user.has_perm('warehouse.read_productwaringrulemodel'):  # 如果当前用户没有查看详情权限
                condtions3 = {} #如果普通用户不具备查看详情权限,则不能查看详情信息
        if self.action == "update":  # 如果是更新列表
            condtions2 = {}
            condtions3 = {}  # 只有创建者可以更新
        if self.action == "partial_update":  # 如果是部分更新列表
            condtions3 = {}  # 只有创建者跟审核者可以部分更新
        return ProductWaringRuleModel.objects.filter(Q(**condtions1) | Q(**condtions2) | Q(**condtions3)).order_by("-id")

