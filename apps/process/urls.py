from django.conf.urls import  include
from django.urls import  path
from rest_framework.routers import DefaultRouter
from apps.process.views.basicinfor_view import *

router = DefaultRouter()
router.register('auditRecord', ProcessAuditRecordView, basename="ProcessAuditRecordView")
router.register('alterRecord', ProcessAlterRecordView, basename="ProcessAlterRecordView")
router.register('image', ProcessImageView, basename="ProcessImageView")
router.register('file', ProcessFileView, basename="ProcessFileView")
router.register('unitType', UnitTypeDefinitionView, basename="UnitTypeDefinitionView")
router.register('unitTypes', UnitTypeDefinitionViews, basename="UnitTypeDefinitionViews")
router.register('unitInfor', UnitInforDefinitionView, basename="UnitInforDefinitionView")
router.register('materialType', MaterialTypeDefinitionView, basename="MaterialTypeDefinitionView")
router.register('materialTypes', MaterialTypeDefinitionViews, basename="MaterialTypeDefinitionViews")
router.register('materialInfor', MaterialInforDefinitionView, basename= "MaterialInforDefinitionView")
router.register('semifinishedType', SemifinishedTypeDefinitionView, basename="SemifinishedTypeDefinitionView")
router.register('semifinishedTypes', SemifinishedTypeDefinitionViews, basename="SemifinishedTypeDefinitionViews")
router.register('semifinishedInfor', SemifinishedInforDefinitionView, basename="SemifinishedInforDefinitionView")
router.register('productType', ProductTypeDefinitionView, basename="ProductTypeDefinitionView")
router.register('productTypes', ProductTypeDefinitionViews, basename="ProductTypeDefinitionViews")
router.register('productInfor', ProductInforDefinitionView, basename="ProductInforDefinitionView")
router.register('stationType', StationTypeDefinitionView, basename="StationTypeDefinitionView")
router.register('stationTypes', StationTypeDefinitionViews, basename="StationTypeDefinitionViews")
router.register('stationMaterial', StationMaterialView, basename="StationMaterialView")
router.register('stationSemifinished', StationSemifinishedView, basename="StationSemifinishedView")
router.register('stationInfor', StationInforDefinitionView, basename="StationInforDefinitionView")
router.register('productRouteType', ProductRouteTypeDefinitionView, basename="ProductRouteTypeDefinitionView")
router.register('productRouteTypes', ProductRouteTypeDefinitionViews, basename="ProductRouteTypeDefinitionViews")
router.register('productRoute', ProductRouteDefinitionView, basename="ProductRouteDefinitionView")
router.register('processInfor', ProcessInforView, basename="ProcessInforView")
router.register('board', ProcessBoardView, basename="ProcessBoardView")
urlpatterns = [
    path(r'', include(router.urls)),
]

