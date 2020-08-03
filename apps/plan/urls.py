from django.conf.urls import  include
from django.urls import  path
from rest_framework.routers import DefaultRouter
from apps.plan.views.basicinfor_view import *

router = DefaultRouter()
router.register('auditRecord', PlanAuditRecordView, basename="PlanAuditRecordView")
router.register('alterRecord', PlanAlterRecordView, basename="PlanAlterRecordView")
router.register('image', PlanImageView, basename="PlanImageView")
router.register('file', PlanFileView, basename="PlanFileView")
router.register('vendorType', VendorTypeDefinitionView, basename= "VendorTypeDefinitionView")
router.register('vendorTypes', VendorTypeDefinitionViews, basename= "VendorTypeDefinitionViews")
router.register('vendorInfor', VendorInforDefinitionView, basename= "VendorInforDefinitionView")
router.register('clientType', ClientTypeDefinitionView, basename="ClientTypeDefinitionView")
router.register('clientTypes', ClientTypeDefinitionViews, basename="ClientTypeDefinitionViews")
router.register('clientInfor', ClientInforDefinitionView, basename="ClientInforDefinitionView")
router.register('salesOrderCreate', SalesOrderCreateView, basename="SalesOrderCreateView")
router.register('salesOrderItemCreate', SalesOrderItemCreateView, basename="SalesOrderItemCreateView")
router.register('productTaskCreate', ProductTaskCreateView, basename="ProductTaskCreateView")
router.register('productTaskItemCreate', ProductTaskItemCreateView, basename="ProductTaskItemCreateView")
router.register('semifinishedTaskCreate', SemifinishedTaskCreateView, basename="SemifinishedTaskCreateView")
router.register('semifinishedTaskItemCreate', SemifinishedTaskItemCreateView, basename="SemifinishedTaskItemCreateView")
router.register('purchaseRequire', PurchaseRequireCreateView, basename="PurchaseRequireCreateView")
router.register('purchaseRequireItem', PurchaseRequireItemCreateView, basename="PurchaseRequireItemCreateView")
router.register('materialManagePlanItem', MaterialManagePlanItemView, basename="MaterialManagePlanItemView")
router.register('materialManagePlan', MaterialManagePlanView, basename="MaterialManagePlanView")
router.register('semifinishedManagePlanItem', SemifinishedManagePlanItemView, basename="SemifinishedManagePlanItemView")
router.register('semifinishedManagePlan', SemifinishedManagePlanView, basename="SemifinishedManagePlanView")
router.register('productManagePlanItem', ProductManagePlanItemView, basename="ProductManagePlanItemView")
router.register('productManagePlan', ProductManagePlanView, basename="ProductManagePlanView")
router.register('equipmentMaintainPlanItem', EquipmentMaintainPlanItemView, basename="EquipmentMaintainPlanItemView")
router.register('equipmentMaintainPlan', EquipmentMaintainPlanView, basename="EquipmentMaintainPlanView")
router.register('board', PlanBoardView, basename="PlanBoardView")

urlpatterns = [
    path(r'', include(router.urls)),
]
