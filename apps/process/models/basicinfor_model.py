from django.db import models

class ProcessAuditRecordModel(models.Model):
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
        db_table = "ProcessAuditRecordModel"
        app_label = 'process'
        verbose_name = "工艺管理－操作记录"
        verbose_name_plural = verbose_name
        permissions={("read_processauditrecordmodel", u"Can read 工艺管理－操作记录")}

class ProcessAlterRecordModel(models.Model):
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
        db_table = "ProcessAlterRecordModel"
        app_label = 'process'
        verbose_name = "工艺管理－审核记录"
        verbose_name_plural = verbose_name

class ProcessImageModel(models.Model):
    """
     当前APP所有的图片项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="process/image/", help_text="当前APP照片")
    image_name=models.CharField(max_length=32,name="image_name", null=True, blank=True, verbose_name="照片名", help_text="当前图片的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前图片属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user",  verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
      return (self.uri+"  >>  "+self.image_name)

    class Meta:
        db_table = "ProcessImageModel"
        app_label = 'process'
        verbose_name = "工艺管理－图片项"
        verbose_name_plural = verbose_name

class ProcessFileModel(models.Model):
    """
    当前APP所有的文件项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    file = models.FileField(upload_to="process/file/", help_text="当前APP文件")
    file_name = models.CharField(max_length=32, name="file_name", null=True, blank=True, verbose_name="文件名", help_text="当前文件的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前文件属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.uri+"  >>  "+self.file_name)

    class Meta:
        db_table = "ProcessFileModel"
        app_label = 'process'
        verbose_name = "工艺管理－文件项"
        verbose_name_plural = verbose_name


class UnitTypeDefinitionModel(models.Model):
    """
    计量单位类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="计量单位类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="计量单位类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="计量单位类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="unitType_child", 
                               on_delete=models.CASCADE,help_text="当前计量单位类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="计量单位附加属性",help_text="当前计量单位类型下计量单位的附加属性")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="计量单位类型文件",help_text="当前计量单位类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "UnitTypeDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－计量单位类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_unittypedefinitionmodel", u"Can read 工艺管理－计量单位类型定义"),
                       ("admin_unittypedefinitionmodel", u"Can admin 工艺管理－计量单位类型定义")}

class UnitInforDefinitionModel(models.Model):
    """
    计量单位定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",help_text="计量单位名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="计量单位编码(与类型联合唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    type = models.ForeignKey(UnitTypeDefinitionModel, on_delete=models.CASCADE,name="type",related_name="unitType_item",
                             verbose_name="类型", help_text="当前计量单位属于的计量单位类型")
    symbol = models.CharField(max_length=16,null=True, blank=True, name="symbol", verbose_name="符号",help_text="计量单位符号")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前计量单位附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前计量单位附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前计量单位附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前计量单位附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前计量单位附加的属性5")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="文件", help_text="当前计量单位的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
       return self.code

    class Meta:
        db_table = "UnitInforDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－计量单位定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_unitinfordefinitionmodel", u"Can read 工艺管理－计量单位定义"),
                       ("admin_unitinfordefinitionmodel", u"Can admin 工艺管理－计量单位定义")}


class MaterialTypeDefinitionModel(models.Model):
    """
    物料类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="物料类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="物料类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="物料类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="materialType_child",
                               on_delete=models.CASCADE,help_text="当前物料类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="物料附加属性",help_text="当前物料类型下物料的附加属性")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="物料类型文件",help_text="当前物料类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "MaterialTypeDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－物料类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_materialtypedefinitionmodel", u"Can read 工艺管理－物料类型定义"),
                       ("admin_materialtypedefinitionmodel", u"Can admin 工艺管理－物料类型定义")}

class MaterialInforDefinitionModel(models.Model):

    """
    物料信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="物料名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码",help_text="物料编码((与类型联合唯一))")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    type = models.ForeignKey(MaterialTypeDefinitionModel, on_delete=models.CASCADE,
                             name="type",related_name="materialType_item", verbose_name="类型", help_text="当前物料属于的物料类型")
    unit = models.ForeignKey(UnitInforDefinitionModel, on_delete=models.CASCADE,name="unit",related_name="unit_material",
                             verbose_name="计量单位", help_text="当前物料使用的计量单位")
    vendor1 = models.CharField(max_length=16, null=True, blank=True, name="vendor1", verbose_name="供应商1", help_text="首选供应商")
    purchase_code1 = models.CharField(max_length=16, null=True, blank=True, name="purchase_code1", verbose_name="采购编码1",
                                      help_text="供应商1采购编码")
    vendor2 = models.CharField(max_length=16, null=True, blank=True, name="vendor2", verbose_name="供应商2",help_text="候选供应商")
    purchase_code2 = models.CharField(max_length=16, null=True, blank=True, name="purchase_code2", verbose_name="采购编码2",
                                      help_text="候选采购编码")
    vendor3 = models.CharField(max_length=16, null=True, blank=True, name="vendor3", verbose_name="供应商3", help_text="备选供应商")
    purchase_code3 = models.CharField(max_length=16, null=True, blank=True, name="purchase_code3", verbose_name="采购编码3",
                                      help_text="备选供应商采购编码")
    character = models.CharField(max_length=32, null=True, blank=True, name="character", verbose_name="质地",help_text="物料质地")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前物料附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前物料附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前物料附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前物料附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前物料附加的属性5")
    attribute6 = models.CharField(max_length=32, null=True, blank=True, name="attribute6", verbose_name="属性6", help_text="当前物料附加的属性6")
    attribute7 = models.CharField(max_length=32, null=True, blank=True, name="attribute7", verbose_name="属性7", help_text="当前物料附件的属性7")
    attribute8 = models.CharField(max_length=32, null=True, blank=True, name="attribute8", verbose_name="属性8", help_text="当前物料附加的属性8")
    attribute9 = models.CharField(max_length=32, null=True, blank=True, name="attribute9", verbose_name="属性9", help_text="当前物料附加的属性9")
    attribute10 = models.CharField(max_length=32, null=True, blank=True, name="attribute10", verbose_name="属性10", help_text="当前物料附加的属性10")
    image = models.ManyToManyField(ProcessImageModel, blank=True, name="image", verbose_name="物料图片", help_text="当前物料的照片信息")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="物料文件",help_text="当前物料的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "MaterialInforDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－物料信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_materialinfordefinitionmodel", u"Can read 工艺管理－物料信息定义"),
                       ("admin_materialinfordefinitionmodel", u"Can admin 工艺管理－物料信息定义")}


class SemifinishedTypeDefinitionModel(models.Model):
    """
    半成品类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="半成品类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="半成品类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="半成品类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="semifinishedType_child",
                               on_delete=models.CASCADE,help_text="当前半成品类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="半成品附加属性",help_text="当前半成品类型下半成品的附加属性")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="半成品类型文件",help_text="当前半成品类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "SemifinishedTypeDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－半成品类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_semifinishedtypedefinitionmodel", u"Can read 工艺管理－半成品类型定义"),
                       ("admin_semifinishedtypedefinitionmodel", u"Can admin 工艺管理－半成品类型定义")}

class SemifinishedInforDefinitionModel(models.Model):
    """
    半成品信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="半成品名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="半成品编码((与类型联合唯一))")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    type = models.ForeignKey(SemifinishedTypeDefinitionModel, on_delete=models.CASCADE, related_name="semifinishedType_item",
                             verbose_name="类型", help_text="当前半成品属于的半成品类型")
    unit = models.ForeignKey(UnitInforDefinitionModel, on_delete=models.CASCADE,related_name="unit_semifinished",
                             verbose_name="计量单位", help_text="当前半成品使用的计量单位")
    routeType_code = models.CharField(max_length=32, null=True, blank=True,name="routeType_code", verbose_name="工艺路线类型编码",
                            help_text="当前项使用的工艺路线类型编码")
    routeType_name = models.CharField(max_length=32, null=True, blank=True,name="routeType_name", verbose_name="工艺路线类型名称",
                            help_text="当前项使用的工艺路线类型名称")
    route_id = models.CharField(max_length=16, null=True, blank=True,name="route_id", verbose_name="工艺路线ID",
                            help_text="当前项使用的工艺路线ID")
    route_code = models.CharField(max_length=32, null=True, blank=True,name="route_code", verbose_name="工艺路线编码",
                            help_text="当前项使用的工艺路线编码")
    route_name = models.CharField(max_length=32, null=True, blank=True,name="route_name", verbose_name="工艺路线名称",
                            help_text="当前项使用的工艺路线名称")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前半成品附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前半成品附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前半成品附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前半成品附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前半成品附加的属性5")
    attribute6 = models.CharField(max_length=32, null=True, blank=True, name="attribute6", verbose_name="属性6", help_text="当前半成品附加的属性6")
    attribute7 = models.CharField(max_length=32, null=True, blank=True, name="attribute7", verbose_name="属性7", help_text="当前半成品附加的属性7")
    attribute8 = models.CharField(max_length=32, null=True, blank=True, name="attribute8", verbose_name="属性8", help_text="当前半成品附加的属性8")
    attribute9 = models.CharField(max_length=32, null=True, blank=True, name="attribute9", verbose_name="属性9", help_text="当前半成品附加的属性9")
    attribute10 = models.CharField(max_length=32, null=True, blank=True, name="attribute10", verbose_name="属性10", help_text="当前半成品附加的属性10")
    image = models.ManyToManyField(ProcessImageModel, blank=True, name="image", verbose_name="半成品图片", help_text="当前半成品的照片信息")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="半成品文件",help_text="当前半成品的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SemifinishedInforDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－半成品信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_semifinishedinfordefinitionmodel", u"Can read 工艺管理－半成品信息定义"),
                       ("admin_semifinishedinfordefinitionmodel", u"Can admin 工艺管理－半成品信息定义")}


class ProductTypeDefinitionModel(models.Model):
    """
    产品类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="产品类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="产品类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="产品类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="productType_child",
                               on_delete=models.CASCADE,help_text="当前产品类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="产品附加属性",help_text="当前产品类型下产品的附加属性")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="产品类型文件",help_text="当前产品类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "ProductTypeDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－产品类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_producttypedefinitionmodel", u"Can read 工艺管理－产品类型定义"),
                       ("admin_producttypedefinitionmodel", u"Can admin 工艺管理－产品类型定义")}

class ProductInforDefinitionModel(models.Model):
    """
    产品信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="产品名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="产品编码((与类型联合唯一))")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    type = models.ForeignKey(ProductTypeDefinitionModel, on_delete=models.CASCADE, related_name="productType_item", verbose_name="类型", help_text="当前产品属于的产品类型")
    unit = models.ForeignKey(UnitInforDefinitionModel, on_delete=models.CASCADE,
                             related_name="unit_product", verbose_name="计量单位", help_text="当前产品使用的计量单位")
    routeType_code = models.CharField(max_length=32, null=True, blank=True,name="routeType_code", verbose_name="工艺路线类型编码",
                            help_text="当前项使用的工艺路线类型编码")
    routeType_name = models.CharField(max_length=32, null=True, blank=True,name="routeType_name", verbose_name="工艺路线类型名称",
                            help_text="当前项使用的工艺路线类型名称")
    route_id = models.CharField(max_length=16, null=True, blank=True,name="route_id", verbose_name="工艺路线ID",
                            help_text="当前项使用的工艺路线ID")
    route_code = models.CharField(max_length=32, null=True, blank=True,name="route_code", verbose_name="工艺路线编码",
                            help_text="当前项使用的工艺路线编码")
    route_name = models.CharField(max_length=32, null=True, blank=True,name="route_name", verbose_name="工艺路线名称",
                            help_text="当前项使用的工艺路线名称")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前产品附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前产品附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前产品附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前产品附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前产品附加的属性5")
    attribute6 = models.CharField(max_length=32, null=True, blank=True, name="attribute6", verbose_name="属性6", help_text="当前产品附加的属性6")
    attribute7 = models.CharField(max_length=32, null=True, blank=True, name="attribute7", verbose_name="属性7", help_text="当前产品附加的属性7")
    attribute8 = models.CharField(max_length=32, null=True, blank=True, name="attribute8", verbose_name="属性8", help_text="当前产品附加的属性8")
    attribute9 = models.CharField(max_length=32, null=True, blank=True, name="attribute9", verbose_name="属性9", help_text="当前产品附加的属性9")
    attribute10 = models.CharField(max_length=32, null=True, blank=True, name="attribute10", verbose_name="属性10", help_text="当前产品附加的属性10")
    image = models.ManyToManyField(ProcessImageModel, blank=True, name="image", verbose_name="产品图片", help_text="当前产品的照片信息")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="产品文件",help_text="当前产品的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ProductInforDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－产品信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_productinfordefinitionmodel", u"Can read 工艺管理－产品信息定义"),
                       ("admin_productinfordefinitionmodel", u"Can admin 工艺管理－产品信息定义")}


class StationTypeDefinitionModel(models.Model):
    """
    工位类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="工位类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="工位类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="工位类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="stationType_child",
                               on_delete=models.CASCADE,help_text="当前工位类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="工位附加属性",help_text="当前工位类型下工位的附加属性")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="工位类型文件",help_text="当前工位类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "StationTypeDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－工位类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_stationtypedefinitionmodel", u"Can read 工艺管理－工位类型定义"),
                       ("admin_stationtypedefinitionmodel", u"Can admin 工艺管理－工位类型定义")}

class StationMaterialModel(models.Model):
    """
    工位物料定义
    """

    id = models.AutoField(primary_key=True, unique=True)
    material = models.ForeignKey(MaterialInforDefinitionModel, name="material", on_delete=models.CASCADE,verbose_name="物料信息",
                                  help_text="物料信息")
    sum = models.FloatField(name="sum", verbose_name="需求数量",help_text="需求数量")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建账号")

    class Meta:
        db_table = "StationMaterialModel"
        app_label = 'process'
        verbose_name = "工艺管理－工位物料定义"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

class StationSemifinishedModel(models.Model):
    """
    工位半成品定义
    """

    id = models.AutoField(primary_key=True, unique=True)
    semifinished = models.ForeignKey(SemifinishedInforDefinitionModel, name="semifinished", on_delete=models.CASCADE,verbose_name="半成品信息",
                                  help_text="半成品信息")
    sum = models.FloatField( name="sum", verbose_name="需求数量",help_text="需求数量")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建账号")

    class Meta:
        db_table = "StationSemifinishedModel"
        app_label = 'process'
        verbose_name = "工艺管理－工位半成品定义"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)

class StationInforDefinitionModel(models.Model):
    """
    工位定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",  help_text="工位名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="工位编码((与类型联合唯一))")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    type = models.ForeignKey(StationTypeDefinitionModel,on_delete=models.CASCADE,related_name="stationType_item",
                             verbose_name="类型", help_text="当前工位属于的工位类型")
    material = models.ManyToManyField(StationMaterialModel, blank=True, name="material", verbose_name="物料",
                                  related_name="stationMaterial_station", help_text="当前工位需要的物料")
    semifinished = models.ManyToManyField(StationSemifinishedModel, blank=True, name="semifinished", verbose_name="物料",
                                          related_name="stationSemifinished_station", help_text="当前工位需要的物料")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前工位附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前工位附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前工位附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前工位附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前工位附加的属性5")
    image = models.ManyToManyField(ProcessImageModel, blank=True, name="image", verbose_name="工位的图片", help_text="当前工位的图片信息")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="工位的文件",help_text="当前工位的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "StationInforDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－工位定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_stationinfordefinitionmodel", u"Can read 工艺管理－工位定义"),
                       ("admin_stationinfordefinitionmodel", u"Can admin 工艺管理－工位定义")}


class ProductRouteTypeDefinitionModel(models.Model):
    """
    生产路线类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="生产路线类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="生产路线类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="生产路线类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="productRouteType_child",
                               on_delete=models.CASCADE,help_text="当前生产路线类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="生产路线附加属性",help_text="当前生产路线类型下生产路线的附加属性")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="生产路线类型文件",help_text="当前生产路线类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "ProductRouteTypeDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－生产路线类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_productroutetypedefinitionmodel", u"Can read 工艺管理－生产路线类型定义"),
                       ("admin_productroutetypedefinitionmodel", u"Can admin 工艺管理－生产路线类型定义")}


class ProductRouteDefinitionModel(models.Model):
    """
    生产路线定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="生产路线名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码",help_text="生产路线编码(与类型联合唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    type = models.ForeignKey(ProductRouteTypeDefinitionModel,on_delete=models.CASCADE,related_name="productRouteType_item",
                             verbose_name="类型", help_text="当前生产路线属于的生产路线类型")
    station = models.ManyToManyField(StationInforDefinitionModel, blank=True, name="station", verbose_name="工位",
                                          related_name="stationInfor_route", help_text="当前路线关联的工位")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前生产路线附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前生产路线附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前生产路线附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前生产路线附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前生产路线附加的属性5")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="生产路线定义文件", help_text="生产路线的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
       return self.code

    class Meta:
        db_table = "ProductRouteDefinitionModel"
        app_label = 'process'
        verbose_name = "工艺管理－生产路线定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_productroutedefinitionmodel", u"Can read 工艺管理－生产路线定义"),
                       ("admin_productroutedefinitionmodel", u"Can admin 工艺管理－生产路线定义"),
                       ("browse_productroutedefinitionmodel", u"Can browse 工艺管理－生产路线定义")}

class ProcessBoardModel(models.Model):
    """
    工艺看板定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="工艺看板名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",help_text="工艺看板编号(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的使用状态")
    image = models.ForeignKey(ProcessImageModel, on_delete=models.CASCADE, name="image",  verbose_name="缩略图", help_text="当前看板的缩略图")
    file = models.ManyToManyField(ProcessFileModel, blank=True, name="file", verbose_name="文件", help_text="当前看板的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProcessAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'ProcessBoardModel'
        app_label = "process"
        verbose_name = "工艺管理－工艺看板定义"
        verbose_name_plural = verbose_name
        permissions = {("read_processboardmodel", u"Can read 工艺管理－工艺看板定义"),
                       ("admin_processboardmodel", u"Can admin 工艺管理－工艺看板定义")}