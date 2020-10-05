from django.db import models

class WarehouseAuditRecordModel(models.Model):
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
        db_table = "WarehouseAuditRecordModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－操作记录"
        verbose_name_plural = verbose_name
        permissions={("read_warehouseauditrecordmodel", u"Can read 仓库管理－操作记录")}

class WarehouseAlterRecordModel(models.Model):
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
        db_table = "WarehouseAlterRecordModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－审核记录"
        verbose_name_plural = verbose_name

class WarehouseImageModel(models.Model):
    """
     当前APP所有的图片项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="warehouse/image/", help_text="当前APP照片")
    image_name=models.CharField(max_length=32,name="image_name", null=True, blank=True, verbose_name="照片名", help_text="当前图片的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前图片属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user",  verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
      return (self.uri+"  >>  "+self.image_name)

    class Meta:
        db_table = "WarehouseImageModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－图片项"
        verbose_name_plural = verbose_name

class WarehouseFileModel(models.Model):
    """
    当前APP所有的文件项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    file = models.FileField(upload_to="warehouse/file/", help_text="当前APP文件")
    file_name = models.CharField(max_length=32, name="file_name", null=True, blank=True, verbose_name="文件名", help_text="当前文件的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前文件属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.uri+"  >>  "+self.file_name)

    class Meta:
        db_table = "WarehouseFileModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－文件项"
        verbose_name_plural = verbose_name

class WarehouseDefinitionModel(models.Model):
    """
    仓库信息定义
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
    TYPE = (
        ("虚拟库", "虚拟库"),
        ("物料库", "物料库"),
        ("半成品库", "半成品库"),
        ("产品库", "产品库"),
        ("设备库", "设备库"),
        ("备品库", "备品库"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="仓库名称(建议唯一)")
    code = models.CharField(max_length=32,unique=True, name="code", verbose_name="编码", help_text="仓库编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16,choices=CLASS, name="classes", verbose_name="类别", help_text="当前仓库处于的层级类别")
    type = models.CharField(max_length=16,choices=TYPE, name="type", default="虚拟库",verbose_name="类型", help_text="当前仓库属于什么类型")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, name="parent",verbose_name="父类别", 
                               related_name="warehouse_child", help_text="当前仓库属于的上一级别")
    position_sum = models.IntegerField(name="position_sum", verbose_name="货位总数", help_text="当前仓库有多少货位")
    image = models.ManyToManyField(WarehouseImageModel, blank=True, name="image", verbose_name="照片", help_text="当前仓库的照片信息")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="文件", help_text="当前仓库的文件信息")
    affiliation = models.CharField(max_length=32, null=True, blank=True, name="affiliation", verbose_name="归属单位",
                                   help_text="当前仓库归属于那个公司/部门")
    location = models.CharField(max_length=32, null=True, blank=True, name="location", verbose_name="地理位置", help_text="当前仓库所在的地理位置(地址)")
    principal = models.CharField(max_length=32, null=True, blank=True, name="principal", verbose_name="责任人",help_text="当前仓库的责任人是谁")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="仓位附加属性",help_text="当前仓库下仓位的附加属性")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=16,  name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32,name="auditor", verbose_name="审核账号",help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录", help_text="当前信息的审核记录")


    def __str__(self):
        return self.code

    class Meta:
        db_table = "WarehouseDefinitionModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－仓库信息定义"
        verbose_name_plural = verbose_name
        permissions = {("read_warehousedefinitionmodel", u"Can read 仓库管理－仓库信息定义"),
                       ("admin_warehousedefinitionmodel", u"Can admin 仓库管理－仓库信息定义")}

class PositionDefinitionModel(models.Model):
    """
    仓位信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("闲置","闲置"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="仓位名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码",help_text="仓位编号((与类型联合唯一))")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="仓位信息的使用状态")
    type = models.ForeignKey(WarehouseDefinitionModel,on_delete=models.CASCADE,name="type", verbose_name="归属仓库",
                               related_name="warehouse_item",help_text="当前仓位归属于的仓库")
    maximum = models.IntegerField(name="maximum", verbose_name="最大容量", help_text="当前仓位可放置的最多物品数量")
    place = models.CharField(max_length=32,name="place",verbose_name="所在位置", help_text="当前仓位所在的位置(在仓库中的位置)")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前仓位的附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前仓位的附件属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前仓位的附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前仓位的附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前仓位的附加属性5")
    image = models.ManyToManyField(WarehouseImageModel, blank=True, name="image", verbose_name="照片", help_text="当前仓位的照片信息")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="文件",help_text="当前仓位的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=16,name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor",verbose_name="审核账号",help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = "PositionDefinitionModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－仓位信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'parent')
        permissions = {("read_positiondefinitionmodel", u"Can read 仓库管理－仓位信息定义"),
                       ("admin_positiondefinitionmodel", u"Can admin 仓库管理－仓位信息定义")}

class WarehouseBoardModel(models.Model):
    """
    仓库看板定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="仓库看板名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",help_text="仓库看板编号(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的使用状态")
    image = models.ForeignKey(WarehouseImageModel, on_delete=models.CASCADE, name="image",  verbose_name="缩略图", help_text="当前看板的缩略图")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="文件", help_text="当前看板的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'WarehouseBoardModel'
        app_label = "warehouse"
        verbose_name = "仓库管理－仓库看板定义"
        verbose_name_plural = verbose_name
        permissions = {("read_warehouseboardmodel", u"Can read 仓库管理－仓库看板定义"),
                       ("admin_warehouseboardmodel", u"Can admin 仓库管理－仓库看板定义")}