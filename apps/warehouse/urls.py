from django.conf.urls import  include
from django.urls import  path
from rest_framework.routers import DefaultRouter
from apps.warehouse.views.basicinfor_view import *
from apps.warehouse.views.inventory_view import *

router = DefaultRouter()
router.register('auditRecord', WarehouseAuditRecordView, basename="WarehouseAuditRecordView")
router.register('alterRecord', WarehouseAlterRecordView, basename="WarehouseAlterRecordView")
router.register('image', WarehouseImageView, basename="WarehouseImageView")
router.register('file', WarehouseFileView, basename="WarehouseFileView")
router.register('warehouse', WarehouseDefinitionView, basename="WarehouseDefinitionView")
router.register('warehouses', WarehouseDefinitionViews, basename="WarehouseDefinitionViews")
router.register('position', PositionDefinitionView, basename="PositionDefinitionView")
router.register('board', WarehouseBoardView, basename="WarehouseBoardView")
router.register('equipmentStockDetail', EquipmentStockDetailView, basename="EquipmentStockDetailView")
router.register('partsStockDetail', PartsStockDetailView ,basename="PartsStockDetailView")
router.register('materialStockDetail', MaterialStockDetailView, basename="MaterialStockDetailView")
router.register('semifinishedStockDetail', SemifinishedStockDetailView, basename="SemifinishedStockDetailView")
router.register('productStockDetail', ProductStockDetailView, basename="ProductStockDetailView")
router.register('equipmentStockInfor', EquipmentStockInforView, basename="EquipmentStockInforView")
router.register('partsStockInfor', PartsStockInforView, basename="PartsStockInforView")
router.register('materialStockInfor', MaterialStockInforView, basename="MaterialStockInforView")
router.register('semifinishedStockInfor', SemifinishedStockInforView, basename="SemifinishedStockInforView")
router.register('productStockInfor', ProductStockInforView, basename="ProductStockInforView")
router.register('equipmentManage', EquipmentManageView, basename="EquipmentManageView")
router.register('partsManage', PartsManageView, basename="PartsManageView")
router.register('materialManage', MaterialManageView, basename="MaterialManageView")
router.register('productManage', ProductManageView, basename="ProductManageView")
router.register('semifinishedManage', SemifinishedManageView, basename="SemifinishedManageView")
router.register('materialWaringRuleItem', MaterialWaringRuleItemView, basename="MaterialWaringRuleItemView")
router.register('materialWaringRule', MaterialWaringRuleView, basename="MaterialWaringRuleView")
router.register('semifinishedWaringRuleItem', SemifinishedWaringRuleItemView, basename="SemifinishedWaringRuleItemView")
router.register('semifinishedWaringRule', SemifinishedWaringRuleView, basename="SemifinishedWaringRuleView")
router.register('productWaringRuleItem', ProductWaringRuleItemView, basename="ProductWaringRuleItemView")
router.register('productWaringRule', ProductWaringRuleView, basename="ProductWaringRuleView")
urlpatterns = [
    path(r'', include(router.urls)),
]
