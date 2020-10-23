from django.contrib import admin

# Register your models1 here.
from apps.lean.models.basicinfor_model import *

admin.site.register(LeanAuditRecordModel)
admin.site.register(LeanAlterRecordModel)
admin.site.register(LeanImageModel)
admin.site.register(LeanFileModel)
admin.site.register(EventTypeDefinitionModel)
admin.site.register(EventInforDefinitionModel)
admin.site.register(LeanBoardModel)