from django_filters.rest_framework import  FilterSet
from apps.equipment.models.recording_model import *


class  PartsUseRecordFilters(FilterSet):
    """
    配件消耗记录
    """
    class Meta:
            model = PartsUseRecordModel
            fields = ["state", "auditor", "create_user"]

class  MaintainRecordFilters(FilterSet):
    """
    维护信息记录
    """
    class Meta:
            model = MaintainRecordModel
            fields = ["state", "auditor", "create_user"]

class EquipmentStateFilters(FilterSet):
    """
    设备状态信息
    """
    class Meta:
            model = EquipmentStateModel
            fields = ["type","create_user"]
