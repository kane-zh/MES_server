from django_filters.rest_framework import  FilterSet
from apps.quality.models.recording_model import *

class RecordInforDefinitionFilters(FilterSet):
    """
    检验记录定义
    """
    class Meta:
        model = InspectionRecordModel
        fields = ["state", "auditor", "create_user", "type"]


