from django.db import models

class QualityAuditRecordModel(models.Model):
    """
     当前APP所有的操作记录
    """
    id = models.AutoField(primary_key=True, unique=True)
    uri = models.CharField(max_length=32, null=True, blank=True, name="uri", verbose_name="资源名称",help_text="当前操作的资源名称")
    uri_id = models.CharField(max_length=16, null=True, blank=True, name="uri_id", verbose_name="资源索引", help_text="当前操作的资源索引项")
    time = models.DateTimeField(auto_now_add=True, verbose_name="时间", help_text="进行操作的时间")
    classes = models.CharField(max_length=16, null=True, blank=True, name="classes", verbose_name="类别",help_text="进行操作的类别")
    user = models.CharField(max_length=32, null=True, blank=True, name="user",verbose_name="账号", help_text="进行操作的账号名称")
    result = models.CharField(max_length=16, null=True, blank=True, name="result", verbose_name="结果", help_text="进行操作的结果")
    content = models.TextField(null=True, blank=True, name="content", verbose_name="内容", help_text="进行当前操作具体涉及哪些内容")

    def __str__(self):
        return self.uri+"  >>  "+self.uri_id

    class Meta:
        db_table = "QualityAuditRecordModel"
        app_label = 'quality'
        verbose_name = "品质管理－操作记录"
        verbose_name_plural = verbose_name
        permissions={("read_qualityauditrecordmodel", u"Can read 品质管理－操作记录")}

class QualityAlterRecordModel(models.Model):
    """
      当前APP所有审核记录
     """
    id = models.AutoField(primary_key=True, unique=True)
    uri = models.CharField(max_length=32, null=True, blank=True,name="uri", verbose_name="资源名称", help_text="当前审核记录属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.uri + "  >>  " + self.create_user)

    class Meta:
        db_table = "QualityAlterRecordModel"
        app_label = 'quality'
        verbose_name = "品质管理－审核记录"
        verbose_name_plural = verbose_name

class QualityImageModel(models.Model):
    """
     当前APP所有的图片项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="quality/image/", help_text="当前APP照片")
    image_name=models.CharField(max_length=32,name="image_name", null=True, blank=True, verbose_name="照片名", help_text="当前图片的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前图片属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user",  verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
      return (self.uri+"  >>  "+self.image_name)

    class Meta:
        db_table = "QualityImageModel"
        app_label = 'quality'
        verbose_name = "品质管理－图片项"
        verbose_name_plural = verbose_name

class QualityFileModel(models.Model):
    """
    当前APP所有的文件项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    file = models.FileField(upload_to="quality/file/", help_text="当前APP文件")
    file_name = models.CharField(max_length=32, name="file_name", null=True, blank=True, verbose_name="文件名", help_text="当前文件的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前文件属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.uri+"  >>  "+self.file_name)

    class Meta:
        db_table = "QualityFileModel"
        app_label = 'quality'
        verbose_name = "品质管理－文件项"
        verbose_name_plural = verbose_name



class DefectTypeDefinitionModel(models.Model):
    """
    缺陷类型定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    CLASS = (
        ("一级类别", "一级类别"),
        ("二级类别", "二级类别"),
        ("三级类别", "三级类别"),
        ("四级类别", "四级类别"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="缺陷类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="缺陷类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="缺陷类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="defectType_child",
                               on_delete=models.CASCADE,help_text="当前缺陷类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="缺陷附加属性",help_text="当前缺陷类型下缺陷的附加属性")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="缺陷类型文件",help_text="当前缺陷类型的文件信息")
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
        db_table = "DefectTypeDefinitionModel"
        app_label = 'quality'
        verbose_name = "品质管理－缺陷类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_defecttypedefinitionmodel", u"Can read 品质管理－缺陷类型定义"),
                       ("admin_defecttypedefinitionmodel", u"Can admin 品质管理－缺陷类型定义")}



class DefectGradeDefinitionModel(models.Model):
    """
    缺陷等级定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="等级名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="等级编码(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    rule = models.TextField(null=True, blank=True, name="rule", verbose_name="评定规则",help_text="此缺陷等级的评定规则是什么")
    influences = models.TextField(null=True, blank=True, name="influences", verbose_name="不良影响",help_text="此等级下的缺陷会产生什么影响")
    processing_method = models.TextField(null=True, blank=True, name="processing_method", verbose_name="处理方式",help_text="此等级下的缺陷产生时,应采取什么处理方式")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="产品文件",help_text="当前缺陷等级的文件信息")
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
        db_table = "DefectGradeDefinitionModel"
        app_label = 'quality'
        verbose_name = "品质管理－缺陷等级定义"
        verbose_name_plural = verbose_name
        permissions = {("read_defectgradedefinitionmodel", u"Can read 品质管理－缺陷等级定义"),
                       ("admin_defectgradedefinitionmodel", u"Can admin 品质管理－缺陷等级定义")}

class DefectInforDefinitionModel(models.Model):

    """
    缺陷信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="缺陷名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码",help_text="缺陷编码((与类型联合唯一))")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的状态")
    type = models.ForeignKey(DefectTypeDefinitionModel, on_delete=models.CASCADE, name="type",related_name="defectType_item",
                             verbose_name="类型", help_text="当前缺陷属于的缺陷类型")
    defect_grade = models.ForeignKey(DefectGradeDefinitionModel, on_delete=models.CASCADE,name="defect_grade",related_name="defectGrade_defectInfor",
                             verbose_name="缺陷等级", help_text="当前缺陷属于的等级")
    rule = models.TextField(null=True, blank=True, name="rule", verbose_name="评定规则",help_text="此缺陷项的评定规则是什么")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前缺陷附件的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前缺陷附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前缺陷附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前缺陷附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前缺陷附加的属性5")
    image = models.ManyToManyField(QualityImageModel, blank=True, name="image", verbose_name="缺陷图片", help_text="当前缺陷的照片信息")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="缺陷文件",help_text="当前缺陷的文件信息")
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
        db_table = "DefectInforDefinitionModel"
        app_label = 'quality'
        verbose_name = "品质管理－缺陷信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_defectinfordefinitionmodel", u"Can read 品质管理－缺陷信息定义"),
                       ("admin_defectinfordefinitionmodel", u"Can admin 品质管理－缺陷信息定义")}


class InspectionStandardTypeDefinitionModel(models.Model):
    """
    检验标准类型定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    CLASS = (
        ("一级类别", "一级类别"),
        ("二级类别", "二级类别"),
        ("三级类别", "三级类别"),
        ("四级类别", "四级类别"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="检验标准类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="检验标准类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="检验标准类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="inspectionStandardType_child",
                               on_delete=models.CASCADE,help_text="当前检验标准类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="检验标准附加属性",help_text="当前检验标准类型下检验标准的附加属性")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="检验标准类型文件",help_text="当前检验标准类型的文件信息")
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
        db_table = "InspectionStandardTypeDefinitionModel"
        app_label = 'quality'
        verbose_name = "品质管理－检验标准类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_inspectionstandardtypedefinitionmodel", u"Can read 品质管理－检验标准类型定义"),
                       ("admin_inspectionstandardtypedefinitionmodel", u"Can admin 品质管理－检验标准类型定义")}


class InspectionStandardDefinitionModel(models.Model):
    """
    检验标准定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",help_text="检验标准名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="检验标准编码(与类型联合唯一)")
    type = models.ForeignKey(InspectionStandardTypeDefinitionModel, on_delete=models.CASCADE,
                             name="type",related_name="inspectionStandardType_item", verbose_name="类型", help_text="当前检验标准属于的检验标准类型")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    defect = models.ManyToManyField(DefectInforDefinitionModel, blank=True, name="defect", verbose_name="缺陷子项",
                                    related_name="defectInfor_inspectionStandard", help_text="当前检验标准的缺陷子项")
    samples_ration= models.IntegerField(name="samples_ration", verbose_name="检验比例",help_text="当前标准要求抽检数量占报检数量的比例")
    ok_ration = models.IntegerField(name="ok_ration", verbose_name="合格比例", help_text="当前标准要求合格数量占抽检数量的比例")
    ng_ration = models.IntegerField(name="ng_ration", verbose_name="不合格比例", help_text="当前标准要求不合格数量占抽检数量的比例")
    concession_ration = models.IntegerField(name="concession_ration", verbose_name="让步接收比例", help_text="当前标准要求让步接收数量占抽检数量的比例")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前检验标准附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前检验标准附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前检验标准附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前检验标准附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前检验标准附加的属性5")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="文件", help_text="当前检验标准的文件信息")
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
        db_table = "InspectionStandardDefinitionModel"
        app_label = 'quality'
        verbose_name = "品质管理－检验标准定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_inspectionstandarddefinitionmodel", u"Can read 品质管理－检验标准定义"),
                       ("admin_inspectionstandarddefinitionmodel", u"Can admin 品质管理－检验标准定义")}


class InspectionReportTypeDefinitionModel(models.Model):
    """
    检验汇报类型定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    CLASS = (
        ("一级类别", "一级类别"),
        ("二级类别", "二级类别"),
        ("三级类别", "三级类别"),
        ("四级类别", "四级类别"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="检验汇报类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="检验汇报类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="检验汇报类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="inspectionReportType_child",
                               on_delete=models.CASCADE,help_text="当前检验汇报类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="检验汇报附加属性",help_text="当前检验汇报类型下检验汇报的附加属性")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="检验汇报类型文件",help_text="当前检验汇报类型的文件信息")
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
        db_table = "InspectionReportTypeDefinitionModel"
        app_label = 'quality'
        verbose_name = "品质管理－检验汇报类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_inspectionreporttypedefinitionmodel", u"Can read 品质管理－检验汇报类型定义"),
                       ("admin_inspectionreporttypedefinitionmodel", u"Can admin 品质管理－检验汇报类型定义")}

class QualityBoardModel(models.Model):
    """
    品质看板定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="品质看板名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",help_text="品质看板编号(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的使用状态")
    image = models.ForeignKey(QualityImageModel, on_delete=models.CASCADE, name="image",  verbose_name="缩略图", help_text="当前看板的缩略图")
    file = models.ManyToManyField(QualityFileModel, blank=True, name="file", verbose_name="文件", help_text="当前看板的文件信息")
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
        db_table = 'QualityBoardModel'
        app_label = "quality"
        verbose_name = "品质管理－品质看板定义"
        verbose_name_plural = verbose_name
        permissions = {("read_qualityboardmodel", u"Can read 品质管理－品质看板定义"),
                       ("admin_qualityboardmodel", u"Can admin 品质管理－品质看板定义")}


