from django.conf.urls import  include
from django.urls import  path
from rest_framework.routers import DefaultRouter
from apps.quality.views.basicinfor_view import *
from apps.quality.views.recording_view import *

router = DefaultRouter()
router.register('auditRecord', QualityAuditRecordView, basename="QualityAuditRecordView")
router.register('alterRecord', QualityAlterRecordView, basename="QualityAlterRecordView")
router.register('image', QualityImageView, basename="QualityImageView")
router.register('file', QualityFileView, basename="QualityFileView")
router.register('defectType', DefectTypeDefinitionView, basename="DefectTypeDefinitionView")
router.register('defectTypes', DefectTypeDefinitionViews, basename="DefectTypeDefinitionViews")
router.register('defectGrade', DefectGradeDefinitionView, basename= "DefectGradeDefinitionView")
router.register('defectInfor', DefectInforDefinitionView, basename= "DefectInforDefinitionView")
router.register('inspectionStandardType', InspectionStandardTypeDefinitionView, basename="InspectionStandardTypeDefinitionView")
router.register('inspectionStandardTypes', InspectionStandardTypeDefinitionViews, basename="InspectionStandardTypeDefinitionViews")
router.register('inspectionStandardInfor', InspectionStandardsDefinitionView, basename="InspectionStandardsDefinitionView")
router.register('inspectionReportType', InspectionReportTypeDefinitionView, basename="InspectionReportTypeDefinitionView")
router.register('inspectionReportTypes', InspectionReportTypeDefinitionViews, basename="InspectionReportTypeDefinitionViews")
router.register('inspectionReportItem', ReportInforItemDefinitionView, basename="ReportInforItemDefinitionView")
router.register('inspectionReport', ReportInforDefinitionView, basename="ReportInforDefinitionView")
router.register('board', QualityBoardView, basename="QualityBoardView")

urlpatterns = [
    path(r'', include(router.urls)),
]
