from django_filters.rest_framework import  FilterSet
from apps.warehouse.models.inventory_model import *

class EquipmentStockDetailFilters(FilterSet):
    """
    设备库存明细
    """
    class Meta:
        model = EquipmentStockDetailModel
        fields=["warehouse_code","equipmentType_code","state"]

class PartsStockDetailFilters(FilterSet):
    """
    设备配件库存明细
    """
    class Meta:
        model = PartsStockDetailModel
        fields=["warehouse_code","partsType_code","state"]

class MaterialStockDetailFilters(FilterSet):
    """
    物料库存明细
    """
    class Meta:
        model = MaterialStockDetailModel
        fields=["warehouse_code","materialType_code","state"]

class SemifinishedStockDetailFilters(FilterSet):
    """
    半成品库存明细
    """
    class Meta:
        model = SemifinishedStockDetailModel
        fields=["warehouse_code","semifinishedType_code","state"]

class ProductStockDetailFilters(FilterSet):
    """
    产品库存明细
    """
    class Meta:
        model = ProductStockDetailModel
        fields=["warehouse_code","productType_code","state"]

class EquipmentStockInforFilters(FilterSet) :
    """
    设备库存信息
    """

    class Meta :
        model = EquipmentStockInforModel
        fields = ["warehouse_code", "equipmentType_code"]

class PartsStockInforFilters(FilterSet) :
    """
    设备配件库存信息
    """

    class Meta :
        model = PartsStockInforModel
        fields = ["warehouse_code", "partsType_code"]

class MaterialStockInforFilters(FilterSet):
    """
    物料库存信息
    """
    class Meta:
        model = MaterialStockInforModel
        fields=["warehouse_code","materialType_code"]

class SemifinishedStockInforFilters(FilterSet):
    """
    半成品库存信息
    """
    class Meta:
        model = SemifinishedStockInforModel
        fields=["warehouse_code","semifinishedType_code"]

class ProductStockInforFilters(FilterSet):
    """
    产品库存信息
    """
    class Meta:
        model = ProductStockInforModel
        fields=["warehouse_code","productType_code"]

class EquipmentManageFilters(FilterSet):
    """
    设备管理
    """
    class Meta:
        model = EquipmentManageModel
        fields=["state","warehouse_code","equipmentType_code", "type","auditor","create_user"]


class PartsManageFilters(FilterSet):
    """
    设备配件管理
    """
    class Meta:
        model = PartsManageModel
        fields=["state","warehouse_code","partsType_code", "type","auditor","create_user"]

class MaterialManageFilters(FilterSet):
    """
    物料管理
    """
    class Meta:
        model = MaterialManageModel
        fields=["state","warehouse_code","materialType_code", "type","auditor","create_user"]

class SemifinishedManageFilters(FilterSet):
    """
    半成品管理
    """
    class Meta:
        model = SemifinishedManageModel
        fields=["state","warehouse_code","semifinishedType_code","type","auditor","create_user"]

class ProductManageFilters(FilterSet):
    """
    产品管理
    """
    class Meta:
        model = ProductManageModel
        fields = ["state", "warehouse_code","productType_code", "type", "auditor","create_user"]

class MaterialWaringRuleFilters(FilterSet):
    """
    物料预警规则
    """
    class Meta:
        model = MaterialWaringRuleModel
        fields = ["state", "auditor", "create_user"]

class SemifinishedWaringRuleFilters(FilterSet):
    """
    半成品预警规则
    """

    class Meta:
        model = SemifinishedWaringRuleModel
        fields = ["state", "auditor", "create_user"]

class ProductWaringRuleFilters(FilterSet):
    """
    产品预警规则
    """

    class Meta:
        model = ProductWaringRuleModel
        fields = ["state", "auditor", "create_user"]

