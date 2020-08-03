from django.contrib import admin

# Register your models1 here.
from apps.equipment.models.basicinfor_model import *
from apps.equipment.models.recording_model import *

admin.site.register(EquipmentAuditRecordModel)
admin.site.register(EquipmentAlterRecordModel)
admin.site.register(EquipmentImageModel)
admin.site.register(EquipmentFileModel)
admin.site.register(EquipmentVendorDefinitionModel)
admin.site.register(PartsTypeDefinitionModel)
admin.site.register(PartsInforDefinitionModel)
admin.site.register(EquipmentTypeDefinitionModel)
admin.site.register(EquipmentAccountModel)
admin.site.register(PartsUseRecordModel)
admin.site.register(MaintainRecordTypeDefinitionModel)
admin.site.register(MaintainRecordModel)
admin.site.register(EquipmentStateModel)
admin.site.register(EquipmentBoardModel)


#

