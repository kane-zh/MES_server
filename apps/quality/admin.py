from django.contrib import admin

from apps.quality.models.basicinfor_model import *
from apps.quality.models.recording_model import *

admin.site.register(QualityAuditRecordModel)
admin.site.register(QualityAlterRecordModel)
admin.site.register(QualityImageModel)
admin.site.register(QualityFileModel)
admin.site.register(DefectTypeDefinitionModel)
admin.site.register(DefectGradeDefinitionModel)
admin.site.register(DefectInforDefinitionModel)
admin.site.register(InspectionStandardTypeDefinitionModel)
admin.site.register(InspectionStandardDefinitionModel)
admin.site.register(InspectionRecordTypeDefinitionModel)
admin.site.register(InspectionRecordItemModel)
admin.site.register(InspectionRecordModel)
admin.site.register(QualityBoardModel)
