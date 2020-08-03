from django_filters.rest_framework import  FilterSet
from apps.lean.models.basicinfor_model import *

class LeanAuditRecordFilters(FilterSet):
    """
    操作记录
    """
    class Meta:
        model = LeanAuditRecordModel
        fields=["uri"]

class LeanBoardFilters(FilterSet):
    """
    精益看板定义
    """
    class Meta:
            model = LeanBoardModel
            fields = ["state", "auditor", "create_user"]