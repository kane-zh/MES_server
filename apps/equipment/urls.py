from django.conf.urls import  include
from django.urls import  path
from rest_framework.routers import DefaultRouter
from apps.equipment.views.basicinfor_view import *
from apps.equipment.views.recording_view import *

router = DefaultRouter()
router.register('auditRecord', EquipmentAuditRecordView, basename="EquipmentAuditRecordView")
router.register('alterRecord', EquipmentAlterRecordView, basename="EquipmentAlterRecordView")
router.register('image', EquipmentImageView, basename="EquipmentImageView")
router.register('file', EquipmentFileView, basename="EquipmentFileView")
router.register('vendor', EquipmentVendorDefinitionView, basename="EquipmentVendorDefinitionView")
router.register('partsType', PartsTypeDefinitionView, basename= "PartsTypeDefinitionView")
router.register('partsTypes', PartsTypeDefinitionViews, basename= "PartsTypeDefinitionViews")
router.register('partsInfor', PartsInforDefinitionView, basename= "PartsInforDefinitionView")
router.register('equipmentType', EquipmentTypeDefinitionView, basename="EquipmentTypeDefinitionView")
router.register('equipmentTypes', EquipmentTypeDefinitionViews, basename="EquipmentTypeDefinitionViews")
router.register('equipmentAccount', EquipmentAccountView, basename="EquipmentAccountView")
router.register('partsUseRecord', PartsUseRecordView, basename="PartsUseRecordView")
router.register('maintainRecordType', MaintainRecordTypeDefinitionView, basename="MaintainRecordTypeDefinitionView")
router.register('maintainRecordTypes', MaintainRecordTypeDefinitionViews, basename="MaintainRecordTypeDefinitionViews")
router.register('maintainRecordItem', MaintainRecordItemView, basename="MaintainRecordItemView")
router.register('maintainRecord', MaintainRecordView, basename="MaintainRecordView")
router.register('equipmentState', EquipmentStateView, basename="EquipmentStateView")
router.register('board', EquipmentBoardView, basename="EquipmentBoardView")

urlpatterns = [
    path(r'', include(router.urls)),
]
