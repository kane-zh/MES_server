from django_filters.rest_framework import  FilterSet
from apps.warehouse.models.basicinfor_model import *

class WarehouseAuditRecordFilters(FilterSet):
    """
    操作记录
    """
    class Meta:
        model = WarehouseAuditRecordModel
        fields=["uri"]

class WarehouseDefinitionFilters(FilterSet):
    """
    仓库信息定义-
    """
    class Meta:
        model = WarehouseDefinitionModel
        fields=["type","classes","state","auditor","create_user"]

class PositionDefinitionFilters(FilterSet):
    """
    仓位信息定义
    """
    class Meta:
        model = PositionDefinitionModel
        fields = ["state", "auditor", "create_user", "parent"]



class WarehouseBoardFilters(FilterSet):

    """
    仓库看板定义
    """
    class Meta:
        model = WarehouseBoardModel
        fields = ["state", "auditor", "create_user"]