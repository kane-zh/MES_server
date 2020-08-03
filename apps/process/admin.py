from django.contrib import admin

# Register your models here.
from apps.process.models.basicinfor_model import *


admin.site.register(ProcessAuditRecordModel)
admin.site.register(ProcessAlterRecordModel)
admin.site.register(ProcessImageModel)
admin.site.register(ProcessFileModel)
admin.site.register(UnitTypeDefinitionModel)
admin.site.register(UnitInforDefinitionModel)
admin.site.register(MaterialTypeDefinitionModel)
admin.site.register(MaterialInforDefinitionModel)
admin.site.register(SemifinishedTypeDefinitionModel)
admin.site.register(SemifinishedInforDefinitionModel)
admin.site.register(ProductTypeDefinitionModel)
admin.site.register(ProductInforDefinitionModel)
admin.site.register(StationTypeDefinitionModel)
admin.site.register(StationMaterialModel)
admin.site.register(StationSemifinishedModel)
admin.site.register(StationInforDefinitionModel)
admin.site.register(ProductRouteTypeDefinitionModel)
admin.site.register(ProductRouteDefinitionModel)
admin.site.register(ProcessBoardModel)

