from django_filters.rest_framework import  FilterSet
from apps.process.models.basicinfor_model import *

class ProcessAuditRecordFilters(FilterSet):
    """
    操作记录
    """
    class Meta:
        model = ProcessAuditRecordModel
        fields=["uri"]

class UnitTypeDefinitionFilters(FilterSet):
    """
    计量单位类型定义
    """
    class Meta:
        model = UnitTypeDefinitionModel
        fields=["state","classes","auditor","create_user"]

class UnitInforDefinitionFilters(FilterSet):
    """
    计量单位定义
    """
    class Meta:
        model = UnitInforDefinitionModel
        fields=["state","auditor","create_user"]


class MaterialTypeDefinitionFilters(FilterSet):
    """
    物料类型定义
    """
    class Meta:
        model = MaterialTypeDefinitionModel
        fields=["state","classes","auditor","create_user"]

class MaterialInforDefinitionFilters(FilterSet):
    """
    物料定义
    """
    class Meta:
        model = MaterialInforDefinitionModel
        fields=["state","auditor","create_user"]

class SemifinishedTypeDefinitionFilters(FilterSet):
    """
    半成品类型定义
    """
    class Meta:
        model = SemifinishedTypeDefinitionModel
        fields = ["state", "classes", "auditor", "create_user"]

class SemifinishedInforDefinitionFilters(FilterSet):
    """
    半成品定义
    """
    class Meta:
        model = SemifinishedInforDefinitionModel
        fields = ["state", "auditor", "create_user"]

class ProductTypeDefinitionFilters(FilterSet):
    """
    产品类型定义
    """
    class Meta:
        model = ProductTypeDefinitionModel
        fields = ["state", "classes", "auditor", "create_user"]

class ProductInforDefinitionFilters(FilterSet):
    """
    产品定义
    """
    class Meta:
        model = ProductInforDefinitionModel
        fields = ["state", "auditor", "create_user"]

class StationTypeDefinitionFilters(FilterSet):
    """
    工位类型定义
    """

    class Meta:
        model = StationTypeDefinitionModel
        fields = ["state", "classes", "auditor", "create_user"]

class StationInforDefinitionFilters(FilterSet):
    """
    工位定义
    """

    class Meta:
        model = StationInforDefinitionModel
        fields = ["state", "auditor", "create_user"]

class ProductRouteTypeDefinitionFilters(FilterSet):
    """
    生产路线类型定义
    """
    class Meta:
        model = ProductRouteTypeDefinitionModel
        fields=["state","classes","auditor","create_user"]

class ProductRouteDefinitionFilters(FilterSet):
    """
    生产路线定义
    """
    class Meta:
        model = ProductRouteDefinitionModel
        fields = ["state", "auditor", "create_user"]


class ProcessBoardFilters(FilterSet):
    """
    工艺看板定义
    """
    class Meta:
        model = ProcessBoardModel
        fields = ["state", "auditor", "create_user"]
