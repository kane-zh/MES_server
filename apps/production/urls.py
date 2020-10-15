from django.conf.urls import  include
from django.urls import  path
from rest_framework.routers import DefaultRouter
from apps.production.views.basicinfor_view import *
from apps.production.views.recording_view import *

router = DefaultRouter()
router.register('auditRecord', ProductionAuditRecordView, basename="ProductionAuditRecordView")
router.register('alterRecord', ProductionAlterRecordView, basename="ProductionAlterRecordView")
router.register('image', ProductionImageView, basename="ProductionImageView")
router.register('file', ProductionFileView, basename="ProductionFileView")
router.register('workshopInfor', WorkshopInforDefinitionView, basename="WorkshopInforDefinitionView")
router.register('workshopInfors', WorkshopInforDefinitionViews, basename="WorkshopInforDefinitionViews")
router.register('teamInfor', TeamInforDefinitionView, basename="TeamInforDefinitionView")
router.register('skillType', SkillTypeDefinitionView, basename="SkillTypeDefinitionView")
router.register('skillTypes', SkillTypeDefinitionViews, basename="SkillTypeDefinitionViews")
router.register('skillInfor', SkillInforDefinitionView, basename="SkillInforDefinitionView")
router.register('personnelInfor', PersonnelInforDefinitionView, basename="PersonnelInforDefinitionView")
router.register('assessmentType', AssessmentTypeDefinitionView, basename="AssessmentTypeDefinitionView")
router.register('assessmentTypes', AssessmentTypeDefinitionViews, basename="AssessmentTypeDefinitionViews")
router.register('productDataType', ProductDataTypeDefinitionView, basename="ProductDataTypeDefinitionView")
router.register('productDataTypes', ProductDataTypeDefinitionViews, basename="ProductDataTypeDefinitionViews")
router.register('semifinishedDataType', SemifinishedDataTypeDefinitionView, basename="SemifinishedDataTypeDefinitionView")
router.register('semifinishedDataTypes', SemifinishedDataTypeDefinitionViews, basename="SemifinishedDataTypeDefinitionViews")
router.register('assessmentLevel', AssessmentLevelDefinitionView, basename="AssessmentLevelDefinitionView")
router.register('assessmentRecord', AssessmentRecordView, basename="AssessmentRecordView")
router.register('productDailyReportItem', ProductDailyReportItemView, basename="ProductDailyReportItemView")
router.register('productDailyReport', ProductDailyReportView, basename="ProductDailyReportView")
router.register('semifinishedDailyReportItem', SemifinishedDailyReportItemView, basename="SemifinishedDailyReportItemView")
router.register('semifinishedDailyReport', SemifinishedDailyReportView, basename="SemifinishedDailyReportView")
router.register('productData', ProductDataDefinitionView, basename="ProductDataDefinitionView")
router.register('semifinishedData', SemifinishedDataDefinitionView, basename="SemifinishedDataDefinitionView")
router.register('board', ProductionBoardView, basename="ProductionBoardView")

urlpatterns = [
    path(r'', include(router.urls)),
]
