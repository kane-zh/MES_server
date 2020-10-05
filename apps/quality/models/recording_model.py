from .basicinfor_model import *
from django.db import models

class InspectionReportItemModel(models.Model):
    """
    检验汇报子项
    """
    id = models.AutoField(primary_key=True, unique=True)
    defect = models.ForeignKey(DefectInforDefinitionModel, name="defect", on_delete=models.CASCADE,verbose_name="缺陷项信息",
                                  help_text="缺陷项信息")
    ok_sum = models.IntegerField(name="ok_sum",null=True, blank=True, verbose_name="合格数量", help_text="合格数量")
    ng_sum = models.IntegerField(name="ng_sum", null=True, blank=True,verbose_name="不合格数量", help_text="不合格数量")
    concession_sum = models.IntegerField(name="concession_sum",null=True, blank=True, verbose_name="让步接收数量", help_text="让步接收数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    image = models.ManyToManyField(QualityImageModel, blank=True, name="image", verbose_name="照片",help_text="当前记录子项的照片信息")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="文件",
                                  help_text="当前记录子项的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建账号")

    class Meta:
        db_table = "InspectionReportItemModel"
        app_label = 'quality'
        verbose_name = "品质管理－检验汇报子项"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
    
class InspectionReportModel(models.Model):
    """
    检验汇报
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    RESULT = (
        ("合格" , "合格"),
        ("不合格", "不合格"),
        ("让步接收", "让步接收"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",help_text="检验汇报名称(建议唯一)")
    code = models.CharField(max_length=32, name="code",null=True, blank=True,  verbose_name="编码", help_text="检验汇报编码(与类型联合唯一)")
    type = models.ForeignKey(InspectionReportTypeDefinitionModel, on_delete=models.CASCADE,name="type",
                             related_name="InspectionReportType_item",verbose_name="类型", help_text="当前检验汇报属于的检验汇报类型")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    child = models.ManyToManyField(InspectionReportItemModel, blank=True, name="child", verbose_name="检验汇报子项",
                                    help_text="当前检验汇报子项")
    submit_sum = models.IntegerField(name="submit_sum", verbose_name="报检数量", help_text="报检数量")
    samples_sum = models.IntegerField(name="samples_sum", verbose_name="检测数量", help_text="检测数量")
    ok_sum = models.IntegerField(name="ok_sum", null=True, blank=True,verbose_name="合格数量", help_text="合格数量")
    ng_sum = models.IntegerField(name="ng_sum", null=True, blank=True,verbose_name="不合格数量", help_text="不合格数量")
    concession_sum = models.IntegerField(name="concession_sum",null=True, blank=True, verbose_name="让步接收数量", help_text="让步接收数量")
    result = models.CharField(max_length=32, choices=RESULT, name="result", verbose_name="检测结果", help_text="检测结果")
    handler = models.CharField(max_length=32,name="handler", null=True, blank=True,verbose_name="操作者", help_text="对当前信息进行操作的是谁")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True, verbose_name="检验时间",  help_text="当前检验的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前检验汇报附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前检验汇报附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前检验汇报附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前检验汇报附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前检验汇报附加的属性5")
    image = models.ManyToManyField(QualityImageModel, blank=True, name="image", verbose_name="照片", help_text="当前记录项的照片信息")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="文件", help_text="当前检验汇报的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(QualityAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
       return self.code

    class Meta:
        db_table = "InspectionReportModel"
        app_label = 'quality'
        verbose_name = "品质管理－检验汇报"
        verbose_name_plural = verbose_name
        permissions = {("read_inspectionreportmodel", u"Can read 品质管理－检验汇报"),
                       ("admin_inspectionreportmodel", u"Can admin 品质管理－检验汇报")}