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


class ProductDataDefinitionFilters(FilterSet):
    """
    产品过程数据定义
    """
    class Meta:
        model = ProductDataDefinitionModel
        fields = ["create_user", "type","productType_code","product_id","taskType_code","task_id"]


class SemifinishedDataDefinitionFilters(FilterSet):
    """
    半成品过程数据定义
    """
    class Meta:
        model = SemifinishedDataDefinitionModel
        fields = ["create_user", "type", "semifinishedType_code","semifinished_id","taskType_code","task_id"]

class ProductStationReportFilters(FilterSet):
    """
    产品工序报工
    """
    class Meta:
        model = ProductStationReportModel
        fields = ["taskType_code", "task_id","productType_code","product_id","stationType_code","station_id"]

class SemifinishedStationReportFilters(FilterSet):
    """
    半成品工序报工
    """
    class Meta:
        model = SemifinishedStationReportModel
        fields = ["taskType_code", "task_id", "semifinishedType_code", "semifinished_id", "stationType_code", "station_id"]








