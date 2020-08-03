from django.db import models
from .basicinfor_model import *

class  AssessmentRecordModel(models.Model):
    """
    考核信息记录
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",help_text="考核记录名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", null=True, blank=True, verbose_name="编码", help_text="考核记录编码(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    type = models.ForeignKey(AssessmentTypeDefinitionModel, on_delete=models.CASCADE,
                             name="type",related_name="assessmentType_item", verbose_name="类型", help_text="当前考核的考核类型")
    personnel = models.ForeignKey(PersonnelInforDefinitionModel, on_delete=models.CASCADE, name="personnel",related_name="personnel_assessment",
                                  verbose_name="人员", help_text="当前考核的人员")
    level = models.ForeignKey(AssessmentLevelDefinitionModel, on_delete=models.CASCADE, name="level",related_name="level_assessment",
                              verbose_name="等级", help_text="当前考核的人的的等级")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="考核时间",help_text="当前考核的时间")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片", help_text="当前记录项的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件", help_text="当前考核记录的文件信息")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前考核附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前考核附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前考核附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前考核附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前考核附加的属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
       return self.code

    class Meta:
        db_table = " AssessmentRecordModel"
        app_label = 'production'
        verbose_name = "生产管理－考核信息记录"
        verbose_name_plural = verbose_name
        permissions = {("read_assessmentrecordmodel", u"Can read 生产管理－考核信息记录"),
                       ("admin_assessmentrecordmodel", u"Can admin 生产管理－考核信息记录")}

class ProductDailyReportItemModel(models.Model):
    """
    产品生产日报子项定义
    """
    id = models.AutoField(primary_key=True, unique=True)
    handler = models.CharField(max_length=32, name="handler", null=True, blank=True, verbose_name="操作者", help_text="对当前信息进行操作的是谁")
    producttask_code= models.CharField(max_length=32, name="producttask_code", null=True, blank=True, verbose_name="生产任务编码", help_text="此项信息关联的生产任务编码")
    producttask_name= models.CharField(max_length=32, name="producttask_name", null=True, blank=True, verbose_name="生产任务名称", help_text="此项信息关联的生产任务编码")
    productType_code = models.CharField(max_length=32, name="productType_code", verbose_name="产品类型编码", help_text="当前信息关联产品类型信息编码")
    productType_name = models.CharField(max_length=32, name="productType_name", verbose_name="产品类型名称", help_text="当前信息关联产品类型信息名称")
    product_id = models.CharField(max_length=32, name="product_id", verbose_name="产品id", help_text="当前信息关联产品信息id")
    product_code = models.CharField(max_length=32, name="product_code", verbose_name="产品编码", help_text="当前信息关联产品信息编码")
    product_name = models.CharField(max_length=32, name="product_name", verbose_name="产品名称", help_text="当前信息关联产品信息名称")
    all_sum = models.IntegerField(name="all_sum", verbose_name="生产总数量", help_text="生产总数量")
    ok_sum = models.IntegerField(name="ok_sum", null=True, blank=True,verbose_name="合格数量", help_text="合格数量")
    ng_sum = models.IntegerField(name="ng_sum", null=True, blank=True,verbose_name="不合格数量", help_text="不合格数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前产品生产日报子项附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前产品生产日报子项附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前产品生产日报子项附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前产品生产日报子项附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前产品生产日报子项附加的属性5")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片", help_text="当前记录子项的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件",help_text="当前记录子项的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建账号")

    class Meta:
        db_table = "ProductDailyReportItemModel"
        app_label = 'production'
        verbose_name = "生产管理－产品生产日报子项定义"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
    
class ProductDailyReportModel(models.Model):
    """
    产品生产日报记录
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="产品生产日报名称(建议唯一)")
    code = models.CharField(max_length=32,  name="code",null=True, blank=True, verbose_name="编码", help_text="产品生产日报编码(与班组联合唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state",
                             verbose_name="状态",help_text="当前信息的状态")
    workshop_code = models.CharField(max_length=32, name="workshop_code", verbose_name="车间编码", help_text="当前日报关联的车间编码")
    workshop_name = models.CharField(max_length=32, name="workshop_name", verbose_name="车间名称", help_text="当前日报关联的车间名称")
    team = models.ForeignKey(TeamInforDefinitionModel, name="team", on_delete=models.CASCADE, verbose_name="班组",
                               help_text="班组")
    child = models.ManyToManyField(ProductDailyReportItemModel, blank=True, name="child",
                                   verbose_name="产品生产日报子项", help_text="当前产品生产日报子项")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前产品生产日报附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前产品生产日报附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前产品生产日报附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前产品生产日报附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前产品生产日报附加的属性5")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片",
                                   help_text="当前记录项的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件",
                                  help_text="当前产品生产日报的文件信息")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="时间", help_text="当前日报的时间")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号",
                                   help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter",
                                   verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ProductDailyReportModel"
        app_label = 'production'
        verbose_name = "生产管理－产品生产日报记录"
        verbose_name_plural = verbose_name
        permissions = {("read_productdailyreportmodel", u"Can read 生产管理－产品生产日报记录"),
                       ("admin_productdailyreportmodel", u"Can admin 生产管理－产品生产日报记录")}
        
class SemifinishedDailyReportItemModel(models.Model):
    """
    半成品生产日报子项定义
    """
    id = models.AutoField(primary_key=True, unique=True)
    handler = models.CharField(max_length=32, name="handler", null=True, blank=True, verbose_name="操作者",
                               help_text="对当前信息进行操作的是谁")
    producttask_code= models.CharField(max_length=32, name="producttask_code", null=True, blank=True, verbose_name="生产任务编码", help_text="此项信息关联的生产任务编码")
    producttask_name= models.CharField(max_length=32, name="producttask_name", null=True, blank=True, verbose_name="生产任务名称", help_text="此项信息关联的生产任务编码")
    semifinishedType_code = models.CharField(max_length=32, name="semifinishedType_code",
                                        verbose_name="半成品类型编码", help_text="当前信息关联半成品类型信息编码")
    semifinishedType_name = models.CharField(max_length=32, name="semifinishedType_name",
                                        verbose_name="半成品类型名称", help_text="当前信息关联半成品类型信息名称")
    semifinished_id = models.CharField(max_length=32, name="semifinished_id", verbose_name="半成品id",
                                  help_text="当前信息关联半成品信息id")
    semifinished_code = models.CharField(max_length=32, name="semifinished_code",  verbose_name="半成品编码",
                                    help_text="当前信息关联半成品信息编码")
    semifinished_name = models.CharField(max_length=32, name="semifinished_name",  verbose_name="半成品名称",
                                    help_text="当前信息关联半成品信息名称")
    all_sum = models.IntegerField(name="all_sum", verbose_name="生产总数量", help_text="生产总数量")
    ok_sum = models.IntegerField(name="ok_sum", null=True, blank=True, verbose_name="合格数量", help_text="合格数量")
    ng_sum = models.IntegerField(name="ng_sum", null=True, blank=True, verbose_name="不合格数量", help_text="不合格数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前半成品生产日报子项附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前半成品生产日报子项附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前半成品生产日报子项附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前半成品生产日报子项附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前半成品生产日报子项附加的属性5")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片",
                                   help_text="当前记录子项的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件",
                                  help_text="当前记录子项的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建账号")

    class Meta:
        db_table = "SemifinishedDailyReportItemModel"
        app_label = 'production'
        verbose_name = "生产管理－半成品生产日报子项定义"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)


class SemifinishedDailyReportModel(models.Model):
    """
    半成品生产日报记录
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="半成品生产日报名称(建议唯一)")
    code = models.CharField(max_length=32, name="code",null=True, blank=True, verbose_name="编码",
                            help_text="半成品生产日报编码(与班组联合唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state",
                             verbose_name="状态", help_text="当前信息的状态")
    workshop_code = models.CharField(max_length=32, name="workshop_code", verbose_name="车间编码", help_text="当前日报关联的车间编码")
    workshop_name = models.CharField(max_length=32, name="workshop_name", verbose_name="车间名称", help_text="当前日报关联的车间名称")
    team = models.ForeignKey(TeamInforDefinitionModel, name="team", on_delete=models.CASCADE, verbose_name="班组",
                             help_text="班组")
    child = models.ManyToManyField(SemifinishedDailyReportItemModel, blank=True, name="child",
                                   verbose_name="半成品生产日报子项",
                                   help_text="当前半成品生产日报子项")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前半成品生产日报附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前半成品生产日报附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前半成品生产日报附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前半成品生产日报附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前半成品生产日报附加的属性5")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片",
                                   help_text="当前记录项的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件",
                                  help_text="当前半成品生产日报的文件信息")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="时间", help_text="当前日报的时间")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号",
                                   help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter",
                                   verbose_name="审核记录", help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SemifinishedDailyReportModel"
        app_label = 'production'
        verbose_name = "生产管理－半成品生产日报记录"
        verbose_name_plural = verbose_name
        permissions = {("read_semifinisheddailyreportmodel", u"Can read 生产管理－半成品生产日报记录"),
                       ("admin_semifinisheddailyreportmodel", u"Can admin 生产管理－半成品生产日报记录")}