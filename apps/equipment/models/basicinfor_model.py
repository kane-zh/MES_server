from django.db import models

class EquipmentAuditRecordModel(models.Model):
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
        db_table = "EquipmentAuditRecordModel"
        app_label = 'equipment'
        verbose_name = "设备管理－操作记录"
        verbose_name_plural = verbose_name
        permissions={("read_equipmentauditrecordmodel", u"Can read 设备管理－操作记录")}

class EquipmentAlterRecordModel(models.Model):
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
        db_table = "EquipmentAlterRecordModel"
        app_label = 'equipment'
        verbose_name = "设备管理－审核记录"
        verbose_name_plural = verbose_name

class EquipmentImageModel(models.Model):
    """
     当前APP所有的图片项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="equipment/image/", help_text="当前APP照片")
    image_name=models.CharField(max_length=32,name="image_name", null=True, blank=True, verbose_name="照片名", help_text="当前图片的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前图片属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user",  verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
      return (self.uri+"  >>  "+self.image_name)

    class Meta:
        db_table = "EquipmentImageModel"
        app_label = 'equipment'
        verbose_name = "设备管理－图片项"
        verbose_name_plural = verbose_name

class EquipmentFileModel(models.Model):
    """
    当前APP所有的文件项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    file = models.FileField(upload_to="equipment/file/", help_text="当前APP文件")
    file_name = models.CharField(max_length=32, name="file_name", null=True, blank=True, verbose_name="文件名", help_text="当前文件的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前文件属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.uri+"  >>  "+self.file_name)

    class Meta:
        db_table = "EquipmentFileModel"
        app_label = 'equipment'
        verbose_name = "设备管理－文件项"
        verbose_name_plural = verbose_name



class EquipmentVendorDefinitionModel(models.Model):
    """
    设备厂商定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="设备供应商(内部)名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="设备供应商(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前设备供应商信息的使用状态")
    image = models.ManyToManyField(EquipmentImageModel, blank=True, name="image", verbose_name="照片",help_text="当前设备供应商的照片信息")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="文件",help_text="当前设备供应商的文件信息")
    address = models.CharField(max_length=32, null=True, blank=True, name="address", verbose_name="地址",help_text="当前设备供应商公司所在的地址")
    mobile = models.CharField(max_length=32, null=True, blank=True, name="mobile", verbose_name="电话", help_text="当前设备供应商联系电话")
    fax = models.CharField(max_length=32, null=True, blank=True, name="fax", verbose_name="传真", help_text="当前设备供应商的传真号码")
    wechat = models.CharField(max_length=32, null=True, blank=True, name="wechat", verbose_name="微信", help_text="当前设备供应商微信号码")
    company_name = models.CharField(max_length=32, null=True, blank=True, name="company_name", verbose_name="公司全称",help_text="当前设备供应商公司全称")
    company_abbre = models.CharField(max_length=32, null=True, blank=True, name="company_abbre", verbose_name="公司简称",help_text="当前设备供应商公司简称")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(EquipmentAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'EquipmentVendorDefinitionModel'
        app_label = "equipment"
        verbose_name = "设备管理－设备厂商定义"
        verbose_name_plural = verbose_name
        permissions = {("read_equipmentvendordefinitionmodel", u"Can read 设备管理－设备厂商定义"),
                       ("admin_equipmentvendordefinitionmodel", u"Can admin 设备管理－设备厂商定义")}

class PartsTypeDefinitionModel(models.Model):
    """
    配件类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="配件类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="配件类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="配件类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="partsType_child",
                               on_delete=models.CASCADE,help_text="当前配件类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="配件附加属性",help_text="当前配件类型下配件的附加属性")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="配件类型文件",help_text="当前配件类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(EquipmentAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "PartsTypeDefinitionModel"
        app_label = 'equipment'
        verbose_name = "设备管理－配件类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_partstypedefinitionmodel", u"Can read 设备管理－配件类型定义"),
                       ("admin_partstypedefinitionmodel", u"Can admin 设备管理－配件类型定义")}

class PartsInforDefinitionModel(models.Model):
    """
    配件信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="配件名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="配件编码(与类型联合唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="配件信息的使用状态")
    type = models.ForeignKey(PartsTypeDefinitionModel, on_delete=models.CASCADE, name="type", related_name="partsType_item",
                             verbose_name="类型", help_text="当前配件属于的类型")
    image = models.ManyToManyField(EquipmentImageModel, blank=True, name="image", verbose_name="照片", help_text="当前配件的照片信息")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="文件", help_text="当前配件的文件信息")
    vendor = models.ForeignKey(EquipmentVendorDefinitionModel, on_delete=models.CASCADE,
                             name="vendor",related_name="vendor_parts", verbose_name="设备厂商", help_text="当前配件的厂商信息")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前配件附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前配件附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前配件附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前配件附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前配件附加的属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32,  name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32,name="auditor", verbose_name="审核账号",help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(EquipmentAlterRecordModel, blank=True, name="alter", verbose_name="审核记录", help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "PartsInforDefinitionModel"
        app_label = 'equipment'
        verbose_name = "设备管理－配件信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_partsinfordefinitionmodel", u"Can read 设备管理－配件信息定义"),
                       ("admin_partsinfordefinitionmodel", u"Can admin 设备管理－配件信息定义")}

class EquipmentTypeDefinitionModel(models.Model):
    """
    设备类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="设备类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="设备类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="设备类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="equipmentType_child",
                               on_delete=models.CASCADE,help_text="当前设备类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="设备附加属性",help_text="当前设备类型下设备的附加属性")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="设备类型文件",help_text="当前设备类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(EquipmentAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "EquipmentTypeDefinitionModel"
        app_label = 'equipment'
        verbose_name = "设备管理－设备类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_equipmenttypedefinitionmodel", u"Can read 设备管理－设备类型定义"),
                       ("admin_equipmenttypedefinitionmodel", u"Can admin 设备管理－设备类型定义")}

class EquipmentAccountModel(models.Model):
    """
    设备信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="设备名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="设备编码((与类型联合唯一))")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="设备信息的使用状态")
    type = models.ForeignKey(EquipmentTypeDefinitionModel, on_delete=models.CASCADE, name="type", related_name="equipmentType_item",
                             verbose_name="类型", help_text="当前设备属于的设备类型")
    vendor = models.ForeignKey(EquipmentVendorDefinitionModel, on_delete=models.CASCADE, name="vendor",related_name="vendor_equipment",
                               verbose_name="设备厂商", help_text="当前设备的厂商信息")
    parts = models.ManyToManyField(PartsInforDefinitionModel, blank=True, name="parts", related_name="parts_equipment",
                                   verbose_name="配件", help_text="当前设备的配件信息")
    image = models.ManyToManyField(EquipmentImageModel, blank=True, name="image", verbose_name="照片", help_text="当前设备的照片信息")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="文件", help_text="当前设备的文件信息")
    affiliation = models.CharField(max_length=32, null=True, blank=True, name="affiliation", verbose_name="归属单位",
                                   help_text="当前设备归属于那个公司/部门")
    location = models.CharField(max_length=32, null=True, blank=True, name="location", verbose_name="地理位置", help_text="当前设备所在的地理位置(地址)")
    principal = models.CharField(max_length=32, null=True, blank=True, name="principal", verbose_name="责任人",help_text="当前设备的责任人是谁")
    depreciationRate = models.CharField(max_length=32, null=True, blank=True, name="depreciationRate", verbose_name="折旧率",
                                help_text="当前设备的折旧率")
    dataOfActivation = models.DateTimeField(verbose_name="启用日期", null=True, blank=True, help_text="当前设备开始使用的时间")
    dataOfPurchase = models.DateTimeField(verbose_name="购买日期", null=True, blank=True,help_text="当前设备购买的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前设备附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前设备附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前设备附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前设备附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前设备附加的属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32,  name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32,name="auditor", verbose_name="审核账号",help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(EquipmentAlterRecordModel, blank=True, name="alter", verbose_name="审核记录", help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "EquipmentAccountModel"
        app_label = 'equipment'
        verbose_name = "设备管理－设备台账定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_equipmentaccountmodel", u"Can read 设备管理－设备台账定义"),
                       ("admin_equipmentaccountmodel", u"Can admin 设备管理－设备台账定义")}


class MaintainRecordTypeDefinitionModel(models.Model):
    """
    维护记录类型定义
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
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="维护记录类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="维护记录类型编码(必须唯一)")
    state = models.CharField(max_length=16,  choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="维护记录类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent",verbose_name="父类别", related_name="maintainRecordType_child",
                               on_delete=models.CASCADE,help_text="当前维护记录类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="维护记录附加属性",help_text="当前维护记录类型下维护记录的附加属性")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="维护记录类型文件",help_text="当前维护记录类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(EquipmentAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
       return self.code

    class Meta:
        db_table = "MaintainRecordTypeDefinitionModel"
        app_label = 'equipment'
        verbose_name = "设备管理－维护记录类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_maintainrecordtypedefinitionmodel", u"Can read 设备管理－维护记录类型定义"),
                       ("admin_maintainrecordtypedefinitionmodel", u"Can admin 设备管理－维护记录类型定义")}

class EquipmentBoardModel(models.Model):
    """
    设备看板定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="设备看板名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",help_text="设备看板编号(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的使用状态")
    image = models.ForeignKey(EquipmentImageModel, on_delete=models.CASCADE, name="image",  verbose_name="缩略图", help_text="当前看板的缩略图")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="文件", help_text="当前看板的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(EquipmentAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'EquipmentBoardModel'
        app_label = "equipment"
        verbose_name = "设备管理－设备看板定义"
        verbose_name_plural = verbose_name
        permissions = {("read_equipmentboardmodel", u"Can read 设备管理－设备看板定义"),
                       ("admin_equipmentboardmodel", u"Can admin 设备管理－设备看板定义")}