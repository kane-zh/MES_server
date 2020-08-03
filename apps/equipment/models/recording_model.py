from .basicinfor_model import *

class PartsUseRecordModel(models.Model):
    """
    配件消耗记录
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="配件消耗记录名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",
                            help_text="配件消耗记录编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="配件消耗记录的使用状态")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="文件",
                                  help_text="当前配件消耗记录的文件信息")
    parts = models.ForeignKey(PartsInforDefinitionModel, name="parts", on_delete=models.CASCADE,verbose_name="备品",
                                  help_text="当前消耗项对应的备品")
    sum = models.IntegerField( name="sum", verbose_name="使用数量",help_text="当前消耗数量")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="使用时间",help_text="当前配件消耗的时间")
    handler = models.CharField(max_length=32, name="handler", null=True, blank=True, verbose_name="操作者",
                               help_text="进行操作的人员是")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前班组的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前班组的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前班组的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前班组的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前班组的属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(EquipmentAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")


    def __str__(self):
       return self.code

    class Meta:
        db_table = "PartsUseRecordModel"
        app_label = 'equipment'
        verbose_name = "设备管理－配件消耗记录"
        verbose_name_plural = verbose_name
        permissions = {("read_partsuserecordmodel", u"Can read 设备管理－配件消耗记录"),
                       ("admin_partsuserecordmodel", u"Can admin 设备管理－配件消耗记录")}


class MaintainRecordItemModel(models.Model):
    """
    维护记录子项
    """
    id = models.AutoField(primary_key=True, unique=True)
    compoment = models.CharField(max_length=32, name="compoment", verbose_name="部件",help_text="进行此次维护消耗的部件")
    method = models.TextField(null=True, blank=True, name="method", verbose_name="维护方法", help_text="维护方法")
    result = models.CharField(max_length=32, name="result",null=True, blank=True,  verbose_name="维护结果", help_text="进行此次维护消耗的结果")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前班组的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前班组的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前班组的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前班组的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前班组的属性5")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="文件", help_text="当前维护记录子项的文件信息")
    image = models.ManyToManyField(EquipmentImageModel, blank=True, name="image", verbose_name="照片",help_text="当前维护记录子项的照片信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "MaintainRecordItemModel"
        app_label = 'equipment'
        verbose_name = "设备管理－维护记录子项"
        verbose_name_plural = verbose_name


class MaintainRecordModel(models.Model):
    """
    维护信息记录
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="维护记录名称(建议唯一)")
    code = models.CharField(max_length=32, name="code",null=True, blank=True,  verbose_name="编码",
                            help_text="维护记录编码(与类型联合唯一)")
    type = models.ForeignKey(MaintainRecordTypeDefinitionModel, on_delete=models.CASCADE,
                             name="type",related_name="maintainRecordType_item", verbose_name="类型", help_text="当前维护的维护类型")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="设备维护信息的使用状态")
    child = models.ManyToManyField(MaintainRecordItemModel, blank=True, name="child", verbose_name="维护记录子项",
                                    help_text="当前检验记录子项")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前维护记录附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前维护记录附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前维护记录附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前维护记录附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前维护记录附加的属性5")
    file = models.ManyToManyField(EquipmentFileModel, blank=True, name="file", verbose_name="文件", help_text="当前维护记录的文件信息")
    image = models.ManyToManyField(EquipmentImageModel, blank=True, name="image", verbose_name="照片",help_text="当前维护记录的照片信息")
    equipment = models.ForeignKey(EquipmentAccountModel, name="equipment", on_delete=models.CASCADE,verbose_name="设备",
                                  related_name="equipment_maintainRecord", help_text="当前维修记录对应的设备")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="维修时间",help_text="当前设备维修的时间")
    handler = models.CharField(max_length=32, name="handler", null=True, blank=True,  verbose_name="操作者", help_text="进行维修的人员是")
    time_consuming=models.CharField(max_length=32, name="time_consuming", null=True, blank=True,  verbose_name="维护耗时", help_text="进行此次维护消耗的时间")
    parts_use=models.ManyToManyField(PartsUseRecordModel, blank=True, name="parts_use", verbose_name="备品消耗",
                                          related_name="partsUserRecord_maintainRecord",help_text="进行当前维护消耗的备品记录")
    result = models.CharField(max_length=32, name="result",null=True, blank=True,  verbose_name="维护结果", help_text="进行此次维护消耗的结果")
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
        db_table = "MaintainRecordModel"
        app_label = 'equipment'
        verbose_name = "设备管理－维护信息记录"
        verbose_name_plural = verbose_name
        permissions = {("read_maintainrecordmodel", u"Can read 设备管理－维护信息记录"),
                       ("admin_maintainrecordmodel", u"Can admin 设备管理－维护信息记录")}


class EquipmentStateModel(models.Model):
    """
    设备状态信息
    """
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="设备状态信息名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",
                            help_text="设备状态信息编码(必须唯一)")
    equipment = models.ForeignKey(EquipmentAccountModel, name="equipment", on_delete=models.CASCADE,verbose_name="设备",help_text="当前记录下的设备")
    state = models.CharField(max_length=32,null=True, blank=True, name="type", verbose_name="状态类型", help_text="当前记录下设备的状态类型")
    runTime = models.CharField(max_length=32, null=True, blank=True, name="runTime", verbose_name="运行时长", help_text="当前记录下设备的运行时长")
    allTime = models.CharField(max_length=32, null=True, blank=True, name="allTime", verbose_name="总时长",help_text="当前记录下设备的总开机时长")
    sum = models.CharField( max_length=32, null=True, blank=True, name="sum",verbose_name="完成数量",help_text="当前完成数量")
    task = models.CharField(max_length=32, null=True, blank=True, name="task", verbose_name="任务号",help_text="当前加工的任务号")
    util_rate = models.CharField(max_length=32,null=True, blank=True,  name="util_rate", verbose_name="稼动率",help_text="当前设备稼动率")
    comp_rate = models.CharField(max_length=32,null=True, blank=True,  name="comp_rate", verbose_name="完成率", help_text="当前设备完成率")
    handler = models.CharField(max_length=32, null=True, blank=True,   name="handler",verbose_name="操作者",help_text="进行操作的人员是")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前设备状态附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前设备状态附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前设备状态附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前设备状态附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前设备状态附加的属性5")
    attribute6 = models.CharField(max_length=32, null=True, blank=True, name="attribute6", verbose_name="属性6", help_text="当前设备状态附加的属性6")
    attribute7 = models.CharField(max_length=32, null=True, blank=True, name="attribute7", verbose_name="属性7", help_text="当前设备状态附加的属性7")
    attribute8 = models.CharField(max_length=32, null=True, blank=True, name="attribute8", verbose_name="属性8", help_text="当前设备状态附加的属性8")
    attribute9 = models.CharField(max_length=32, null=True, blank=True, name="attribute9", verbose_name="属性9", help_text="当前设备状态附加的属性9")
    attribute10 = models.CharField(max_length=32, null=True, blank=True, name="attribute10", verbose_name="属性10", help_text="当前设备状态附加的属性10")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "EquipmentStateModel"
        app_label = 'equipment'
        verbose_name = "设备管理－设备状态信息"
        verbose_name_plural = verbose_name
        permissions = {("read_equipmentstatemodel", u"Can read 设备管理－设备状态信息"),
                       ("admin_equipmentstatemodel", u"Can admin 设备管理－设备状态信息")}
