from django_filters.rest_framework import  FilterSet
from apps.equipment.models.basicinfor_model import *

class EquipmentAuditRecordFilters(FilterSet):
    """
    操作记录
    """
    class Meta:
        model = EquipmentAuditRecordModel
        fields=["uri"]

class EquipmentVendorDefinitionFilters(FilterSet):
    """
    设备厂商定义
    """
    class Meta:
        model = EquipmentVendorDefinitionModel
        fields = ["state", "auditor", "create_user"]

class PartsTypeDefinitionFilters(FilterSet):
    """
    配件类型定义
    """
    class Meta:
        model = PartsTypeDefinitionModel
        fields = ["state","classes", "auditor", "create_user"]
class PartsInforDefinitionFilters(FilterSet):
    """
    配件信息定义
    """
    class Meta:
            model = PartsInforDefinitionModel
            fields = ["state", "auditor", "create_user"]

class EquipmentTypeDefinitionFilters(FilterSet):
    """
    设备类型定义
    """
    class Meta:
        model = EquipmentTypeDefinitionModel
        fields = ["state","classes", "auditor", "create_user"]
class EquipmentAccountFilters(FilterSet):
    """
    设备台账定义
    """
    class Meta:
            model = EquipmentAccountModel
            fields = ["state", "auditor", "create_user"]

class MaintainRecordTypeDefinitionFilters(FilterSet):
    """
    维护记录类型定义
    """
    class Meta:
        model = MaintainRecordTypeDefinitionModel
        fields = ["state","classes", "auditor", "create_user"]

class EquipmentBoardFilters(FilterSet):
    """
    设备看板定义
    """
    class Meta:
            model = EquipmentBoardModel
            fields = ["state", "auditor", "create_user"]