from django_filters.rest_framework import  FilterSet
from apps.quality.models.recording_model import *

class ReportInforDefinitionFilters(FilterSet):
    """
    检验汇报定义
    """
    class Meta:
        model = InspectionReportModel
        fields = ["state", "auditor", "create_user", "type"]


