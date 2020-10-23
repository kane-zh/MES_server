from django_filters.rest_framework import  FilterSet
from apps.lean.models.basicinfor_model import *

class LeanAuditRecordFilters(FilterSet):
    """
    操作记录
    """
    class Meta:
        model = LeanAuditRecordModel
        fields=["uri"]
class EventTypeDefinitionFilters(FilterSet):
    """
    事件类型定义
    """
    class Meta:
        model = EventTypeDefinitionModel
        fields=["state","classes","auditor","create_user"]

class EventInforDefinitionFilters(FilterSet):
    """
    事件信息定义
    """
    class Meta:
        model = EventInforDefinitionModel
        fields=["state","create_user","type"]

class LeanBoardFilters(FilterSet):
    """
    精益看板定义
    """
    class Meta:
            model = LeanBoardModel
            fields = ["state", "auditor", "create_user"]