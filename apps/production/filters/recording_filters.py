from django_filters.rest_framework import  FilterSet
from apps.production.models.recording_model import *


class AssessmentRecordFilters(FilterSet):
    """
    考核记录
    """
    class Meta:
        model = AssessmentRecordModel
        fields = ["state", "auditor", "create_user", "type","personnel"]

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


class ProductdDataDefinitionFilters(FilterSet):
    """
    产品过程数据定义
    """
    class Meta:
        model = ProductDataDefinitionModel
        fields = ["create_user", "type","product_id"]


class SemifinishedDataDefinitionFilters(FilterSet):
    """
    半成品过程数据定义
    """

    class Meta:
        model = SemifinishedDataDefinitionModel
        fields = ["create_user", "type", "semifinished_id"]