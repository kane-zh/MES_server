from django_filters.rest_framework import  FilterSet
from apps.plan.models.basicinfor_model import *

class PlanAuditRecordFilters(FilterSet):
    """
    操作记录
    """
    class Meta:
        model = PlanAuditRecordModel
        fields=["uri"]
class VendorTypeDefinitionFilters(FilterSet):
    """
    供应商类型定义
    """
    class Meta:
        model = VendorTypeDefinitionModel
        fields=["state","classes","auditor","create_user"]

class VendorInforDefinitionFilters(FilterSet):
    """
    供应商信息定义
    """
    class Meta:
        model = VendorInforDefinitionModel
        fields=["state","auditor","create_user","type"]

class ClientTypeDefinitionFilters(FilterSet):
    """
    客户类型定义
    """
    class Meta:
        model = ClientTypeDefinitionModel
        fields=["state","classes","auditor","create_user"]

class ClientInforDefinitionFilters(FilterSet):

    """
    客户信息定义
    """
    class Meta:
        model = ClientInforDefinitionModel
        fields=["state","auditor","create_user","type"]
class SalesOrderCreateFilters(FilterSet):
    """
    销售订单创建
    """
    class Meta:
        model = SalesOrderCreateModel
        fields = ["state", "auditor", "create_user"]

class ProductTaskTypeFilters(FilterSet):
    """
    产品生产任务类型定义
    """
    class Meta:
        model = ProductTaskTypeModel
        fields=["state","classes","auditor","create_user"]

class ProductTaskCreateFilters(FilterSet):
    """
    产品生产任务单创建
    """
    class Meta:
        model = ProductTaskCreateModel
        fields = ["state", "type","auditor", "create_user","priority","workshop_code"]
class SemifinishedTaskTypeFilters(FilterSet):
    """
    半成品生产任务类型定义
    """
    class Meta:
        model = SemifinishedTaskTypeModel
        fields=["state","classes","auditor","create_user"]

class SemifinishedTaskCreateFilters(FilterSet):
    """
    半成品生产任务单创建
    """
    class Meta:
        model = SemifinishedTaskCreateModel
        fields = ["state","type","auditor", "create_user","priority","workshop_code"]

class PurchaseRequireCreateFilters(FilterSet):
    """
    采购需求单创建
    """
    class Meta:
        model = PurchaseRequireCreateModel
        fields = ["state", "auditor", "create_user"]

class MaterialManagePlanFilters(FilterSet):
    """
    物料管理计划创建
    """
    class Meta:
        model = MaterialManagePlanModel
        fields = ["state", "auditor", "create_user","priority"]

class SemifinishedManagePlanFilters(FilterSet):
    """
    半成品管理计划创建
    """
    class Meta:
        model = SemifinishedManagePlanModel
        fields = ["state", "auditor", "create_user","priority"]

class ProductManagePlanFilters(FilterSet):
    """
    产品管理计划创建
    """
    class Meta:
        model = ProductManagePlanModel
        fields = ["state", "auditor", "create_user","priority"]

class EquipmentMaintainPlanFilters(FilterSet):
    """
    设备维护计划
    """
    class Meta:
            model = EquipmentMaintainPlanModel
            fields = ["state", "auditor", "create_user"]

class PlanBoardFilters(FilterSet):
    """
    计划看板定义
    """
    class Meta:
        model = PlanBoardModel
        fields = ["state", "auditor", "create_user"]