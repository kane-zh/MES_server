from django_filters.rest_framework import  FilterSet
from apps.production.models.recording_model import *


class AssessmentRecordFilters(FilterSet):
    """
    考核记录
    """
    class Meta:
        model = AssessmentRecordModel
        fields = ["state", "auditor", "create_user", "type"]

class ProductDailyReportFilters(FilterSet):
    """
    产品生产日报记录
    """
    class Meta:
        model = ProductDailyReportModel
        fields = ["state", "auditor", "create_user"]

class SemifinishedDailyReportFilters(FilterSet):
    """
    半成品生产日报记录
    """
    class Meta:
        model = SemifinishedDailyReportModel
        fields = ["state", "auditor", "create_user"]