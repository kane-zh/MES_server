from django.contrib import admin

# Register your models1 here
from apps.warehouse.models.basicinfor_model import *
from apps.warehouse.models.inventory_model import *

admin.site.register(WarehouseAuditRecordModel)
admin.site.register(WarehouseAlterRecordModel)
admin.site.register(WarehouseImageModel)
admin.site.register(WarehouseFileModel)
admin.site.register(WarehouseDefinitionModel)
admin.site.register(PositionDefinitionModel)
admin.site.register(WarehouseBoardModel)
admin.site.register(EquipmentStockDetailModel)
admin.site.register(PartsStockDetailModel)
admin.site.register(MaterialStockDetailModel)
admin.site.register(SemifinishedStockDetailModel)
admin.site.register(ProductStockDetailModel)
admin.site.register(EquipmentStockInforModel)
admin.site.register(PartsStockInforModel)
admin.site.register(MaterialStockInforModel)
admin.site.register(SemifinishedStockInforModel)
admin.site.register(ProductStockInforModel)
admin.site.register(EquipmentManageModel)
admin.site.register(PartsManageModel)
admin.site.register(MaterialManageModel)
admin.site.register(SemifinishedManageModel)
admin.site.register(ProductManageModel)
admin.site.register(MaterialWaringRuleItemModel)
admin.site.register(MaterialWaringRuleModel)
admin.site.register(SemifinishedWaringRuleItemModel)
admin.site.register(SemifinishedWaringRuleModel)
admin.site.register(ProductWaringRuleItemModel)
admin.site.register(ProductWaringRuleModel)
