from django.contrib import admin

# Register your models1 here.
from apps.production.models.basicinfor_model import *
from apps.production.models.recording_model import  *
admin.site.register(ProductionAuditRecordModel)
admin.site.register(ProductionAlterRecordModel)
admin.site.register(ProductionImageModel)
admin.site.register(ProductionFileModel)
admin.site.register(WorkshopInforDefinitionModel)
admin.site.register(TeamInforDefinitionModel)
admin.site.register(SkillTypeDefinitionModel)
admin.site.register(SkillInforDefinitionModel)
admin.site.register(PersonnelInforDefinitionModel)
admin.site.register(AssessmentTypeDefinitionModel)
admin.site.register(AssessmentLevelDefinitionModel)
admin.site.register(AssessmentRecordModel)
admin.site.register(ProductDailyReportItemModel)
admin.site.register(ProductDailyReportModel)
admin.site.register(SemifinishedDailyReportItemModel)
admin.site.register(SemifinishedDailyReportModel)
admin.site.register(ProductionBoardModel)