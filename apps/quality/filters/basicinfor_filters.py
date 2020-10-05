from django_filters.rest_framework import  FilterSet
from apps.quality.models.basicinfor_model import *

class QualityAuditRecordFilters(FilterSet):
    """
    操作记录
    """
    class Meta:
        model = QualityAuditRecordModel
        fields=["uri"]

class DefectTypeDefinitionFilters(FilterSet):
    """
    缺陷类型定义
    """
    class Meta:
        model = DefectTypeDefinitionModel
        fields=["state","classes","auditor","create_user"]

class DefectGradeDefinitionFilters(FilterSet):
    """
    缺陷等级定义
    """
    class Meta:
        model = DefectGradeDefinitionModel
        fields=["state","auditor","create_user"]

class DefectInforDefinitionFilters(FilterSet):
    """
    缺陷定义
    """
    class Meta:
        model = DefectInforDefinitionModel
        fields=["state","auditor","create_user","type"]

class InspectionStandardTypeDefinitionFilters(FilterSet):
    """
    检验标准类型定义
    """
    class Meta:
        model = InspectionStandardTypeDefinitionModel
        fields=["state","classes","auditor","create_user"]

class InspectionStandardsDefinitionFilters(FilterSet):
    """
    检验标准定义
    """
    class Meta:
        model = InspectionStandardDefinitionModel
        fields=["state","auditor","create_user","type"]

class InspectionReportTypeDefinitionFilters(FilterSet):
    """
    检验汇报类型定义
    """
    class Meta:
        model = InspectionReportTypeDefinitionModel
        fields = ["state", "classes", "auditor", "create_user"]

class QualityBoardFilters(FilterSet):
    """
    品质看板定义
    """
    class Meta:
            model = QualityBoardModel
            fields = ["state", "auditor", "create_user"]