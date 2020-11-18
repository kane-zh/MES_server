from django.db import models

class PlanAuditRecordModel(models.Model):
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
        db_table = "PlanAuditRecordModel"
        app_label = 'plan'
        verbose_name = "计划管理－操作记录"
        verbose_name_plural = verbose_name
        permissions={("read_planauditrecordmodel", u"Can read 计划管理－操作记录")}

class PlanAlterRecordModel(models.Model):
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
        db_table = "PlanAlterRecordModel"
        app_label = 'plan'
        verbose_name = "计划管理－审核记录"
        verbose_name_plural = verbose_name

class PlanImageModel(models.Model):
    """
     当前APP所有的图片项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="plan/image/", help_text="当前APP照片")
    image_name=models.CharField(max_length=32,name="image_name", null=True, blank=True, verbose_name="照片名", help_text="当前图片的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前图片属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user",  verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
      return (self.uri+"  >>  "+self.image_name)

    class Meta:
        db_table = "PlanImageModel"
        app_label = 'plan'
        verbose_name = "计划管理－图片项"
        verbose_name_plural = verbose_name

class PlanFileModel(models.Model):
    """
    当前APP所有的文件项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    file = models.FileField(upload_to="plan/file/", help_text="当前APP文件")
    file_name = models.CharField(max_length=32, name="file_name", null=True, blank=True, verbose_name="文件名", help_text="当前文件的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前文件属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.uri+"  >>  "+self.file_name)

    class Meta:
        db_table = "PlanFileModel"
        app_label = 'plan'
        verbose_name = "计划管理－文件项"
        verbose_name_plural = verbose_name


class VendorTypeDefinitionModel(models.Model):
    """
    供应商类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="供应商类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="供应商类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别",
                               help_text="供应商类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="vendorType_child",
                               on_delete=models.CASCADE, help_text="当前供应商类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="供应商附加属性",
                                        help_text="当前供应商类型下供应商的附加属性")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="供应商类型文件",
                                  help_text="当前供应商类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "VendorTypeDefinitionModel"
        app_label = 'plan'
        verbose_name = "计划管理－供应商类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_vendortypedefinitionmodel", u"Can read 计划管理－供应商类型定义"),
                       ("admin_vendortypedefinitionmodel", u"Can admin 计划管理－供应商类型定义")}


class VendorInforDefinitionModel(models.Model):
    """
    供应商信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="供应商(内部)名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="供应商编号((与类型联合唯一))")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前供应商信息的使用状态")
    type = models.ForeignKey(VendorTypeDefinitionModel, on_delete=models.CASCADE,
                             name="type", related_name="vendorType_item", verbose_name="类型", help_text="当前客户属于的客户类型")
    image = models.ManyToManyField(PlanImageModel, blank=True, name="image", verbose_name="照片",
                                   help_text="当前供应商的照片信息")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件",
                                  help_text="当前供应商的文件信息")
    address = models.CharField(max_length=32, null=True, blank=True, name="address", verbose_name="地址",
                               help_text="当前供应商公司所在的地址")
    mobile = models.CharField(max_length=32, null=True, blank=True, name="mobile", verbose_name="电话",
                              help_text="当前供应商联系电话")
    fax = models.CharField(max_length=32, null=True, blank=True, name="fax", verbose_name="传真", help_text="当前供应商的传真号码")
    wechat = models.CharField(max_length=32, null=True, blank=True, name="wechat", verbose_name="微信",
                              help_text="当前供应商微信号码")
    company_name = models.CharField(max_length=32, null=True, blank=True, name="company_name", verbose_name="公司全称",
                                    help_text="当前供应商公司全称")
    company_abbre = models.CharField(max_length=32, null=True, blank=True, name="company_abbre", verbose_name="公司简称",
                                     help_text="当前供应商公司简称")
    qualification = models.CharField(max_length=32, null=True, blank=True, name="qualification", verbose_name="资质",
                                     help_text="当前供应商具有的资质")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前供应商附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前供应商附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前供应商附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前供应商附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前供应商附加的属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'VendorInforDefinitionModel'
        app_label = "plan"
        verbose_name = "计划管理－供应商信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_vendorinfordefinitionmodel", u"Can read 计划管理－供应商信息定义"),
                       ("admin_vendorinfordefinitionmodel", u"Can admin 计划管理－供应商信息定义")}


class ClientTypeDefinitionModel(models.Model):
    """
    客户类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="客户类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="客户类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="客户类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="clientType_child",on_delete=models.CASCADE, help_text="当前客户类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="客户附加属性",
                                        help_text="当前客户类型下客户的附加属性")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="客户类型文件",
                                  help_text="当前客户类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ClientTypeDefinitionModel"
        app_label = 'plan'
        verbose_name = "计划管理－客户类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_clienttypedefinitionmodel", u"Can read 计划管理－客户类型定义"),
                       ("admin_clienttypedefinitionmodel", u"Can admin 计划管理－客户类型定义")}


class ClientInforDefinitionModel(models.Model):
    """
    客户信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="客户(内部)名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="客户编号((与类型联合唯一))")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前客户信息的使用状态")
    type = models.ForeignKey(ClientTypeDefinitionModel, on_delete=models.CASCADE,
                             name="type", related_name="clientType_item", verbose_name="类型", help_text="当前客户属于的客户类型")
    image = models.ManyToManyField(PlanImageModel, blank=True, name="image", verbose_name="照片",
                                   help_text="当前客户的照片信息")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", help_text="当前客户的文件信息")
    address = models.CharField(max_length=32, null=True, blank=True, name="address", verbose_name="地址",
                               help_text="当前客户公司所在的地址")
    mobile = models.CharField(max_length=32, null=True, blank=True, name="mobile", verbose_name="电话",
                              help_text="当前客户联系电话")
    fax = models.CharField(max_length=32, null=True, blank=True, name="fax", verbose_name="传真", help_text="当前客户的传真号码")
    wechat = models.CharField(max_length=32, null=True, blank=True, name="wechat", verbose_name="微信",
                              help_text="当前客户微信号码")
    company_name = models.CharField(max_length=32, null=True, blank=True, name="company_name", verbose_name="公司全称",
                                    help_text="当前客户公司全称")
    company_abbre = models.CharField(max_length=32, null=True, blank=True, name="company_abbre", verbose_name="公司简称",
                                     help_text="当前客户公司简称")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前客户附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前客户附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前客户附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前客户附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前客户附加的属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'ClientInforDefinitionModel'
        app_label = "plan"
        verbose_name = "计划管理－客户信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_clientinfordefinitionmodel", u"Can read 计划管理－客户信息定义"),
                       ("admin_clientinfordefinitionmodel", u"Can admin 计划管理－客户信息定义")}


class  SalesOrderItemCreateModel(models.Model):
    """
    销售订单子项创建
    """
    STATUS = (
        ("新建", "新建"),
        ("等待", "等待"),
        ("终止", "终止"),
        ("完成", "完成")
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    productType_code = models.CharField(max_length=32, name="productType_code", verbose_name="产品类型编码", help_text="当前信息关联产品类型信息编码")
    productType_name = models.CharField(max_length=32, name="productType_name", verbose_name="产品类型名称", help_text="当前信息关联产品类型信息名称")
    product_id = models.CharField(max_length=32, name="product_id", verbose_name="产品ID", help_text="当前订单项对应的产品ID")
    product_name = models.CharField(max_length=32, name="product_name", verbose_name="产品名称",help_text="当前订单项对应的产品名称")
    product_code = models.CharField(max_length=32, name="product_code", verbose_name="产品编码",help_text="当前订单项对应的产品编码")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="批次号", help_text="当前产品的批次")
    sum = models.IntegerField(name="sum", verbose_name="产品数量", help_text="当前项需要的产品数量")
    assigned = models.IntegerField(name="assigned", default=0, null=True, blank=True, verbose_name="已分配数量", help_text="当前项已分配给生产任务的数量")
    completed = models.IntegerField(name="completed",default=0, null=True, blank=True, verbose_name="完成数量", help_text="当前项已完成的数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件",related_name="salesOrderItem_file", help_text="创建订单子项使用的文件")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.product_code + "  >>  "+ self.product_name)

    class Meta:
        db_table = "SalesOrderItemCreateModel"
        app_label = 'plan'
        verbose_name = "计划管理－销售订单子项定义"
        verbose_name_plural = verbose_name

class SalesOrderCreateModel(models.Model):
    """
    销售订单创建
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("终止", "终止"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="销售订单名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="销售订单编码(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",
                             verbose_name="状态", help_text="当前信息的状态")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件",help_text="创建销售订单使用的文件")
    client = models.ForeignKey(ClientInforDefinitionModel, on_delete=models.CASCADE,name="client",
                              verbose_name="销售订单归属的客户", related_name="client_SalesOrder",help_text="当前销售订单归属的客户")
    delivery_time = models.DateTimeField(verbose_name="交付日期",help_text="当前订单需要的交付日期")
    child=models.ManyToManyField(SalesOrderItemCreateModel, blank=True, name="child",related_name="salesOrderItem_parent" ,verbose_name="子项", help_text="当前订单的子包含项")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间",help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号",  help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SalesOrderCreateModel"
        app_label = 'plan'
        verbose_name = "计划管理－销售订单定义"
        verbose_name_plural = verbose_name
        permissions = {("read_salesordercreatemodel", u"Can read 计划管理－销售订单定义"),
                       ("admin_salesordercreatemodel", u"Can admin 计划管理－销售订单定义"),
                       ("deal_salesordercreatemodel", u"Can deal 计划管理－销售订单定义")}

class ProductTaskTypeModel(models.Model):
    """
    产品生产类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="产品生产任务类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="产品生产任务类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="产品生产任务类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="productTaskType_child",on_delete=models.CASCADE, help_text="当前产品生产任务类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="产品生产任务附加属性",
                                        help_text="当前产品生产任务类型下产品生产任务的附加属性")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="产品生产任务类型文件",
                                  help_text="当前产品生产任务类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ProductTaskTypeModel"
        app_label = 'plan'
        verbose_name = "计划管理－产品生产任务类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_producttasktypemodel", u"Can read 计划管理－产品生产任务类型定义"),
                       ("admin_producttasktypemodel", u"Can admin 计划管理－产品生产任务类型定义")}

class   ProductTaskItemCreateModel(models.Model):
    """
    产品生产任务单子项创建
    """
    STATUS = (
        ("新建", "新建"),
        ("等待", "等待"),
        ("加工中", "加工中"),
        ("终止", "终止"),
        ("挂起", "挂起"),
        ("完成", "完成")
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    salesOrderItem = models.ForeignKey(SalesOrderItemCreateModel, on_delete=models.CASCADE,name="salesOrderItem",
                              verbose_name="归属销售订单子项", related_name="salesOrderItem_productTaskItem",help_text="当前产品生产任务单子项归属的销售订单子项")
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
    equipmentType_code = models.CharField(max_length=32, null=True, blank=True, name="equipmentType_code",
                                          verbose_name="设备类型编码",
                                          help_text="当前项使用的设备类型编码")
    equipmentType_name = models.CharField(max_length=32, null=True, blank=True, name="equipmentType_name",
                                          verbose_name="设备类型名称",
                                          help_text="当前项使用的设备类型名称")
    equipment_id = models.CharField(max_length=16, null=True, blank=True, name="equipment_id", verbose_name="设备ID",
                                    help_text="当前项使用的设备ID")
    equipment_code = models.CharField(max_length=32, null=True, blank=True, name="equipment_code", verbose_name="设备编码",
                                      help_text="当前项使用的设备编码")
    equipment_name = models.CharField(max_length=32, null=True, blank=True, name="equipment_name", verbose_name="设备名称",
                                      help_text="当前项使用的设备名称")
    team_id = models.CharField(max_length=16, null=True, blank=True, name="team_id", verbose_name="班组ID",
                               help_text="当前项使用的班组ID")
    team_code = models.CharField(max_length=32, null=True, blank=True, name="team_code", verbose_name="班组编码",
                                 help_text="当前项使用的班组编码")
    team_name = models.CharField(max_length=32, null=True, blank=True, name="team_name", verbose_name="班组名称",
                                 help_text="当前项使用的班组名称")
    sum = models.IntegerField(name="sum", verbose_name="数量", help_text="当前生产任务单子项需求数量")
    completed = models.IntegerField(name="completed",default=0, null=True, blank=True,    verbose_name="完成数量", help_text="当前生产任务单子项完成数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    attribute6 = models.CharField(max_length=32, null=True, blank=True, name="attribute6", verbose_name="属性6", help_text="当前附加属性6")
    attribute7 = models.CharField(max_length=32, null=True, blank=True, name="attribute7", verbose_name="属性7", help_text="当前附加属性7")
    attribute8 = models.CharField(max_length=32, null=True, blank=True, name="attribute8", verbose_name="属性8", help_text="当前附加属性8")
    attribute9 = models.CharField(max_length=32, null=True, blank=True, name="attribute9", verbose_name="属性9", help_text="当前附加属性9")
    attribute10 = models.CharField(max_length=32, null=True, blank=True, name="attribute10", verbose_name="属性10", help_text="当前附加属性10")
    attribute11 = models.CharField(max_length=32, null=True, blank=True, name="attribute11", verbose_name="属性11", help_text="当前附加属性11")
    attribute12 = models.CharField(max_length=32, null=True, blank=True, name="attribute12", verbose_name="属性12", help_text="当前附加属性12")
    attribute13 = models.CharField(max_length=32, null=True, blank=True, name="attribute13", verbose_name="属性13", help_text="当前附加属性13")
    attribute14 = models.CharField(max_length=32, null=True, blank=True, name="attribute14", verbose_name="属性14", help_text="当前附加属性14")
    attribute15 = models.CharField(max_length=32, null=True, blank=True, name="attribute15", verbose_name="属性15", help_text="当前附加属性15")
    attribute16 = models.CharField(max_length=32, null=True, blank=True, name="attribute16", verbose_name="属性16", help_text="当前附加属性16")
    attribute17 = models.CharField(max_length=32, null=True, blank=True, name="attribute17", verbose_name="属性17", help_text="当前附加属性17")
    attribute18 = models.CharField(max_length=32, null=True, blank=True, name="attribute18", verbose_name="属性18", help_text="当前附加属性18")
    attribute19 = models.CharField(max_length=32, null=True, blank=True, name="attribute19", verbose_name="属性19", help_text="当前附加属性19")
    attribute20 = models.CharField(max_length=32, null=True, blank=True, name="attribute20", verbose_name="属性20", help_text="当前附加属性20")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件",
                                  related_name="productTaskItem_file", help_text="创建产品生产任务单子项使用的文件")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",
                                       help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间",
                                       help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32,name="create_user",verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "ProductTaskItemCreateModel"
        app_label = 'plan'
        verbose_name = "计划管理－产品生产任务单子项创建"
        verbose_name_plural = verbose_name
        permissions = {("read_producttaskitemcreatemodel", u"Can read 计划管理－产品生产任务单子项创建"),
                       ("admin_producttaskitemcreatemodel", u"Can admin 计划管理－产品生产任务单子项创建")}

class ProductTaskCreateModel(models.Model):
    """
    产品生产任务单创建
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("终止", "终止"),
        ("挂起", "挂起"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    PRIORITY = (
        ("正常", "正常"),
        ("优先", "优先"),
        ("紧急", "紧急"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32,name="name",null=True, blank=True, verbose_name="名称",help_text="生产任务单名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="产品生产任务单编码(必须唯一)")
    state = models.CharField(max_length=16, null=True, blank=True, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    type = models.ForeignKey(ProductTaskTypeModel, on_delete=models.CASCADE,name="type", related_name="productTaskType_item", verbose_name="类型",
                             help_text="当前产品生产任务属于的产品生产任务类型")
    priority = models.CharField(max_length=16, choices=PRIORITY, default="正常", name="priority", verbose_name="优先级",
                             help_text="当前信息的优先级")
    delivery_time = models.DateTimeField(verbose_name="交付日期",help_text="当前生产需要的交付日期")
    workshop_code= models.CharField(max_length=32, name="workshop_code", null=True, blank=True, verbose_name="车间编码", help_text="此项任务指定的生产车间编码")
    workshop_name= models.CharField(max_length=32, name="workshop_name", null=True, blank=True, verbose_name="车间名称", help_text="此项任务指定的生产车间名称")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    child=models.ManyToManyField(ProductTaskItemCreateModel, blank=True, name="child", verbose_name="子项",related_name="productTaskItem_parent" ,
                                  help_text="当前订单的子包含项")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", related_name="productionTask_file", help_text="创建生产任务单使用的文件")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",
                                       help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间",
                                       help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ProductTaskCreateModel"
        app_label = 'plan'
        verbose_name = "计划管理－产品生产任务单定义"
        verbose_name_plural = verbose_name
        permissions = {("read_producttaskcreatemodel", u"Can read 计划管理－产品生产任务单创建"),
                       ("admin_producttaskcreatemodel", u"Can admin 计划管理－产品生产任务单创建"),
                       ("deal_producttaskcreatemodel", u"Can deal 计划管理－产品生产任务单创建")}

class SemifinishedTaskTypeModel(models.Model):
    """
    半成品生产类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="半成品生产任务类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="半成品生产任务类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="半成品生产任务类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="semifinishedTaskType_child",on_delete=models.CASCADE, help_text="当前半成品生产任务类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="半成品生产任务附加属性",
                                        help_text="当前半成品生产任务类型下半成品生产任务的附加属性")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="半成品生产任务类型文件",
                                  help_text="当前半成品生产任务类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SemifinishedTaskTypeModel"
        app_label = 'plan'
        verbose_name = "计划管理－半成品生产任务类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_semifinishedtasktypemodel", u"Can read 计划管理－半成品生产任务类型定义"),
                       ("admin_semifinishedtasktypemodel", u"Can admin 计划管理－半成品生产任务类型定义")}

class   SemifinishedTaskItemCreateModel(models.Model):
    """
    半成品生产任务单子项创建
    """
    STATUS = (
        ("新建", "新建"),
        ("等待", "等待"),
        ("加工中", "加工中"),
        ("终止", "终止"),
        ("挂起", "挂起"),
        ("完成", "完成")
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    semifinishedType_code = models.CharField(max_length=32, name="semifinishedType_code", verbose_name="半成品类型编码",
                                           help_text="当前信息关联半成品类型信息编码")
    semifinishedType_name = models.CharField(max_length=32, name="semifinishedType_name", verbose_name="半成品类型名称",
                                           help_text="当前信息关联半成品类型信息名称")
    semifinished_id = models.CharField(max_length=32, name="semifinished_id", verbose_name="半成品ID",
                                     help_text="当前订单项对应的半成品ID")
    semifinished_name = models.CharField(max_length=32, name="semifinished_name", verbose_name="半成品名称",
                                       help_text="当前订单项对应的半成品名称")
    semifinished_code = models.CharField(max_length=32, name="semifinished_code", verbose_name="半成品编码",
                                       help_text="当前订单项对应的半成品编码")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="批次号", help_text="当前半成品的批次")
    routeType_code = models.CharField(max_length=32, null=True, blank=True, name="routeType_code",
                                      verbose_name="工艺路线类型编码",
                                      help_text="当前项使用的工艺路线类型编码")
    routeType_name = models.CharField(max_length=32, null=True, blank=True, name="routeType_name",
                                      verbose_name="工艺路线类型名称",
                                      help_text="当前项使用的工艺路线类型名称")
    route_id = models.CharField(max_length=16, null=True, blank=True, name="route_id", verbose_name="工艺路线ID",
                                help_text="当前项使用的工艺路线ID")
    route_code = models.CharField(max_length=32, null=True, blank=True, name="route_code", verbose_name="工艺路线编码",
                                  help_text="当前项使用的工艺路线编码")
    route_name = models.CharField(max_length=32, null=True, blank=True, name="route_name", verbose_name="工艺路线名称",
                                  help_text="当前项使用的工艺路线名称")
    equipmentType_code = models.CharField(max_length=32, null=True, blank=True, name="equipmentType_code",
                                          verbose_name="设备类型编码",
                                          help_text="当前项使用的设备类型编码")
    equipmentType_name = models.CharField(max_length=32, null=True, blank=True, name="equipmentType_name",
                                          verbose_name="设备类型名称",
                                          help_text="当前项使用的设备类型名称")
    equipment_id = models.CharField(max_length=16, null=True, blank=True, name="equipment_id", verbose_name="设备ID",
                                    help_text="当前项使用的设备ID")
    equipment_code = models.CharField(max_length=32, null=True, blank=True, name="equipment_code", verbose_name="设备编码",
                                      help_text="当前项使用的设备编码")
    equipment_name = models.CharField(max_length=32, null=True, blank=True, name="equipment_name", verbose_name="设备名称",
                                      help_text="当前项使用的设备名称")
    team_id = models.CharField(max_length=16, null=True, blank=True, name="team_id", verbose_name="班组ID",
                               help_text="当前项使用的班组ID")
    team_code = models.CharField(max_length=32, null=True, blank=True, name="team_code", verbose_name="班组编码",
                                 help_text="当前项使用的班组编码")
    team_name = models.CharField(max_length=32, null=True, blank=True, name="team_name", verbose_name="班组名称",
                                 help_text="当前项使用的班组名称")
    sum = models.IntegerField(name="sum", verbose_name="半成品数量", help_text="当前项需要的半成品数量")
    completed = models.IntegerField(name="completed",default=0, null=True, blank=True,    verbose_name="完成数量", help_text="当前生产任务单子项完成数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    attribute6 = models.CharField(max_length=32, null=True, blank=True, name="attribute6", verbose_name="属性6", help_text="当前附加属性6")
    attribute7 = models.CharField(max_length=32, null=True, blank=True, name="attribute7", verbose_name="属性7", help_text="当前附加属性7")
    attribute8 = models.CharField(max_length=32, null=True, blank=True, name="attribute8", verbose_name="属性8", help_text="当前附加属性8")
    attribute9 = models.CharField(max_length=32, null=True, blank=True, name="attribute9", verbose_name="属性9", help_text="当前附加属性9")
    attribute10 = models.CharField(max_length=32, null=True, blank=True, name="attribute10", verbose_name="属性10", help_text="当前附加属性10")
    attribute11 = models.CharField(max_length=32, null=True, blank=True, name="attribute11", verbose_name="属性11", help_text="当前附加属性11")
    attribute12 = models.CharField(max_length=32, null=True, blank=True, name="attribute12", verbose_name="属性12", help_text="当前附加属性12")
    attribute13 = models.CharField(max_length=32, null=True, blank=True, name="attribute13", verbose_name="属性13", help_text="当前附加属性13")
    attribute14 = models.CharField(max_length=32, null=True, blank=True, name="attribute14", verbose_name="属性14", help_text="当前附加属性14")
    attribute15 = models.CharField(max_length=32, null=True, blank=True, name="attribute15", verbose_name="属性15", help_text="当前附加属性15")
    attribute16 = models.CharField(max_length=32, null=True, blank=True, name="attribute16", verbose_name="属性16", help_text="当前附加属性16")
    attribute17 = models.CharField(max_length=32, null=True, blank=True, name="attribute17", verbose_name="属性17", help_text="当前附加属性17")
    attribute18 = models.CharField(max_length=32, null=True, blank=True, name="attribute18", verbose_name="属性18", help_text="当前附加属性18")
    attribute19 = models.CharField(max_length=32, null=True, blank=True, name="attribute19", verbose_name="属性19", help_text="当前附加属性19")
    attribute20 = models.CharField(max_length=32, null=True, blank=True, name="attribute20", verbose_name="属性20", help_text="当前附加属性20")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件",
                                  related_name="semifinishedTaskItem_file", help_text="创建半成品生产任务单子项使用的文件")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",
                                       help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间",
                                       help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32,name="create_user",verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "SemifinishedTaskItemCreateModel"
        app_label = 'plan'
        verbose_name = "计划管理－半成品生产任务单子项创建"
        verbose_name_plural = verbose_name
        permissions = {("read_semifinishedtaskitemcreatemodel", u"Can read 计划管理－半成品生产任务单子项创建"),
                       ("admin_semifinishedtaskitemcreatemodel", u"Can admin 计划管理－半成品生产任务单子项创建")}

class SemifinishedTaskCreateModel(models.Model):
    """
    半成品生产任务单创建
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("终止", "终止"),
        ("挂起", "挂起"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    PRIORITY = (
        ("正常", "正常"),
        ("优先", "优先"),
        ("紧急", "紧急"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32,name="name",null=True, blank=True, verbose_name="名称",help_text="生产任务单名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="半成品生产任务单编码(必须唯一)")
    state = models.CharField(max_length=16, null=True, blank=True, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    type = models.ForeignKey(SemifinishedTaskTypeModel, on_delete=models.CASCADE,name="type", related_name="semifinishedTaskType_item", verbose_name="类型",
                             help_text="当前半成品生产任务属于的半成品生产任务类型")
    priority = models.CharField(max_length=16, choices=PRIORITY, default="正常", name="priority", verbose_name="优先级",
                             help_text="当前信息的优先级")
    delivery_time = models.DateTimeField(verbose_name="交付日期",help_text="当前生产需要的交付日期")
    workshop_code= models.CharField(max_length=32, name="workshop_code", null=True, blank=True, verbose_name="车间编码", help_text="此项任务指定的生产车间编码")
    workshop_name= models.CharField(max_length=32, name="workshop_name", null=True, blank=True, verbose_name="车间名称", help_text="此项任务指定的生产车间名称")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    child=models.ManyToManyField(SemifinishedTaskItemCreateModel, blank=True, name="child", verbose_name="子项",related_name="semifinishedTaskItem_parent" ,
                                  help_text="当前订单的子包含项")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", related_name="semifinishedionTask_file", help_text="创建生产任务单使用的文件")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",
                                       help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间",
                                       help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SemifinishedTaskCreateModel"
        app_label = 'plan'
        verbose_name = "计划管理－半成品生产任务单定义"
        verbose_name_plural = verbose_name
        permissions = {("read_ssemifinishedtaskcreatemodel", u"Can read 计划管理－半成品生产任务单创建"),
                       ("admin_semifinishedtaskcreatemodel", u"Can admin 计划管理－半成品生产任务单创建"),
                       ("deal_semifinishedtaskcreatemodel", u"Can deal 计划管理－半成品生产任务单创建")}
class   PurchaseRequireItemCreateModel(models.Model):
    """
    采购需求单子项创建
    """
    STATUS = (
        ("新建", "新建"),
        ("等待", "等待"),
        ("终止", "终止"),
        ("完成", "完成")
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    materialType_code = models.CharField(max_length=32, name="materialType_code", verbose_name="物料类型编码", help_text="当前信息关联物料类型信息编码")
    materialType_name = models.CharField(max_length=32, name="materialType_name", verbose_name="物料类型名称", help_text="当前信息关联物料类型信息名称")
    material_id = models.CharField(max_length=32, name="material_id", verbose_name="物料ID", help_text="当前订单项对应的物料ID")
    material_name = models.CharField(max_length=32, name="material_name", verbose_name="物料名称",help_text="当前订单项对应的物料名称")
    material_code = models.CharField(max_length=32, name="material_code", verbose_name="物料编码",help_text="当前订单项对应的物料编码")
    sum = models.IntegerField(name="sum", verbose_name="物料数量", help_text="当前项需要的物料数量")
    vendor = models.ForeignKey(VendorInforDefinitionModel, on_delete=models.CASCADE,name="vendor",
                              verbose_name="此项物料指定的供应商", related_name="vendor_purchaseRequire",help_text="当前此项物料指定的供应商")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件",
                                  related_name="purchaseRequireItem_file", help_text="创建当前信息使用的文件")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号",help_text="创建当前信息的账号名称")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "PurchaseRequireItemCreateModel"
        app_label = 'plan'
        verbose_name = "计划管理－采购需求单子项创建"
        verbose_name_plural = verbose_name


class PurchaseRequireCreateModel(models.Model):
    """
    采购需求单创建
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("挂起", "挂起"),
        ("终止", "终止"),
        ("完成", "完成"),
        ("作废", "作废"),
    )

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="采购需求单子项名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="采购需求单子项编码(必须唯一)")
    state = models.CharField(max_length=16, null=True, blank=True, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    child=models.ManyToManyField(PurchaseRequireItemCreateModel, blank=True, name="child",related_name="purchaseRequireItem_parent" , verbose_name="子项",
                                   help_text="当前订单的子包含项")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="需求日期",help_text="当前物料需求单项需求日期")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件",
                                  related_name="purchaseRequire_file", help_text="创建当前信息使用的文件")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",
                                       help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间",
                                       help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=16,  name="create_user",verbose_name="创建账号",
                                   help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=16, null=True, blank=True, name="auditor", verbose_name="审核账号",
                               help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "PurchaseRequireCreateModel"
        app_label = 'plan'
        verbose_name = "计划管理－采购需求单创建"
        verbose_name_plural = verbose_name
        permissions = {("read_purchaserequirecreatemodel", u"Can read 计划管理－采购需求单创建"),
                       ("admin_purchaserequirecreatemodel", u"Can admin 计划管理－采购需求单创建"),
                       ("deal_purchaserequirecreatemodel", u"Can deal 计划管理－采购需求单创建")}

class MaterialManagePlanItemModel(models.Model):
    """
    物料管理计划子项
    """
    OPERATING_TYPE = (
        ("入库操作", "入库操作"),
        ("出库操作", "出库操作"),
        ("盘点管理", "盘点管理"),
    )
    STATUS = (
        ("新建", "新建"),
        ("等待", "等待"),
        ("终止", "终止"),
        ("完成", "完成")
    )
    id = models.AutoField(primary_key=True, unique=True)
    type = models.CharField(max_length=16, choices=OPERATING_TYPE, name="type", verbose_name="类型",help_text="当前操作记录属于的操作记录类型")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    materialType_code = models.CharField(max_length=32, name="materialType_code", verbose_name="物料类型编码", help_text="当前信息关联物料类型信息编码")
    materialType_name = models.CharField(max_length=32, name="materialType_name", verbose_name="物料类型名称", help_text="当前信息关联物料类型信息名称")
    material_id = models.CharField(max_length=32, name="material_id", verbose_name="物料ID", help_text="当前订单项对应的物料ID")
    material_name = models.CharField(max_length=32, name="material_name", verbose_name="物料名称",help_text="当前订单项对应的物料名称")
    material_code = models.CharField(max_length=32, name="material_code", verbose_name="物料编码",help_text="当前订单项对应的物料编码")
    sum = models.IntegerField(name="sum", verbose_name="物料数量", help_text="当前项需要的物料数量")
    completed = models.IntegerField(name="completed",default=0, null=True, blank=True, verbose_name="完成数量", help_text="当前项已完成的数量")
    batch = models.CharField(max_length=32, null=True, blank=True, name="batch", verbose_name="物料批次", help_text="当前物料的批次")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.material_code + "  >>  " + self.material_name)

    class Meta:
        db_table = "MaterialManagePlanItemModel"
        app_label = 'plan'
        verbose_name = "计划管理－物料管理计划子项"
        verbose_name_plural = verbose_name

class MaterialManagePlanModel(models.Model):
    """
    物料管理计划
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("挂起", "挂起"),
        ("终止", "终止"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    PRIORITY = (
        ("正常", "正常"),
        ("优先", "优先"),
        ("紧急", "紧急"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="物料管理计划(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="物料管理计划(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的状态")
    priority = models.CharField(max_length=16, choices=PRIORITY, default="正常", name="priority", verbose_name="优先级",
                             help_text="当前信息的优先级")
    child = models.ManyToManyField(MaterialManagePlanItemModel, blank=True, name="child",related_name="materialManageItem_parent" , verbose_name="物料管理计划子项",help_text="当前物料管理计划子项")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="执行时间",help_text="当前任务执行的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", help_text="当前操作的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "MaterialManagePlanModel"
        app_label = 'plan'
        verbose_name = "计划管理－物料管理计划"
        verbose_name_plural = verbose_name
        permissions = {("read_materialmanageplanmodel", u"Can read 计划管理－物料管理计划"),
                       ("admin_materialmanageplanmodel", u"Can admin 计划管理－物料管理计划"),
                       ("deal_materialmanageplanmodel", u"Can deal 计划管理－物料管理计划")}

class SemifinishedManagePlanItemModel(models.Model):
    """
    半成品管理计划子项
    """
    OPERATING_TYPE = (
        ("入库操作", "入库操作"),
        ("出库操作", "出库操作"),
        ("盘点管理", "盘点管理"),
    )
    STATUS = (
        ("新建", "新建"),
        ("等待", "等待"),
        ("终止", "终止"),
        ("完成", "完成")
    )
    id = models.AutoField(primary_key=True, unique=True)
    type = models.CharField(max_length=16, choices=OPERATING_TYPE, name="type", verbose_name="类型",help_text="当前操作记录属于的操作记录类型")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    semifinishedType_code = models.CharField(max_length=32, name="semifinishedType_code", verbose_name="半成品类型编码", help_text="当前信息关联半成品类型信息编码")
    semifinishedType_name = models.CharField(max_length=32, name="semifinishedType_name", verbose_name="半成品类型名称", help_text="当前信息关联半成品类型信息名称")
    semifinished_id = models.CharField(max_length=32, name="semifinished_id", verbose_name="半成品ID", help_text="当前订单项对应的半成品ID")
    semifinished_name = models.CharField(max_length=32, name="semifinished_name", verbose_name="半成品名称",help_text="当前订单项对应的半成品名称")
    semifinished_code = models.CharField(max_length=32, name="semifinished_code", verbose_name="半成品编码",help_text="当前订单项对应的半成品编码")
    sum = models.IntegerField(name="sum", verbose_name="半成品数量", help_text="当前项需要的半成品数量")
    completed = models.IntegerField(name="completed",default=0, null=True, blank=True, verbose_name="完成数量", help_text="当前项已完成的数量")
    batch = models.CharField(max_length=32, null=True, blank=True, name="batch", verbose_name="半成品批次", help_text="当前半成品的批次")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.semifinished_code + "  >>  " + self.semifinished_name)

    class Meta:
        db_table = "SemifinishedManagePlanItemModel"
        app_label = 'plan'
        verbose_name = "计划管理－半成品管理计划子项"
        verbose_name_plural = verbose_name

class SemifinishedManagePlanModel(models.Model):
    """
    半成品管理计划
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("挂起", "挂起"),
        ("终止", "终止"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    PRIORITY = (
        ("正常", "正常"),
        ("优先", "优先"),
        ("紧急", "紧急"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="半成品管理计划(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="半成品管理计划(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的状态")
    priority = models.CharField(max_length=16, choices=PRIORITY, default="正常", name="priority", verbose_name="优先级",
                             help_text="当前信息的优先级")
    child = models.ManyToManyField(SemifinishedManagePlanItemModel, blank=True, name="child",related_name="semifinishedManageItem_parent" , verbose_name="半成品管理计划子项",help_text="当前半成品管理计划子项")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="执行时间",help_text="当前任务执行的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", help_text="当前操作的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SemifinishedManagePlanModel"
        app_label = 'plan'
        verbose_name = "计划管理－半成品管理计划"
        verbose_name_plural = verbose_name
        permissions = {("read_semifinishedmanageplanmodel", u"Can read 计划管理－半成品管理计划"),
                       ("admin_semifinishedmanageplanmodel", u"Can admin 计划管理－半成品管理计划"),
                       ("deal_semifinishedmanageplanmodel", u"Can deal 计划管理－半成品管理计划")}

class ProductManagePlanItemModel(models.Model):
    """
    产品管理计划子项
    """
    OPERATING_TYPE = (
        ("入库操作", "入库操作"),
        ("出库操作", "出库操作"),
        ("盘点管理", "盘点管理"),
    )
    STATUS = (
        ("新建", "新建"),
        ("等待", "等待"),
        ("终止", "终止"),
        ("完成", "完成")
    )
    id = models.AutoField(primary_key=True, unique=True)
    type = models.CharField(max_length=16, choices=OPERATING_TYPE, name="type", verbose_name="类型",help_text="当前操作记录属于的操作记录类型")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    productType_code = models.CharField(max_length=32, name="productType_code", verbose_name="产品类型编码", help_text="当前信息关联产品类型信息编码")
    productType_name = models.CharField(max_length=32, name="productType_name", verbose_name="产品类型名称", help_text="当前信息关联产品类型信息名称")
    product_id = models.CharField(max_length=32, name="product_id", verbose_name="产品ID", help_text="当前订单项对应的产品ID")
    product_name = models.CharField(max_length=32, name="product_name", verbose_name="产品名称",help_text="当前订单项对应的产品名称")
    product_code = models.CharField(max_length=32, name="product_code", verbose_name="产品编码",help_text="当前订单项对应的产品编码")
    sum = models.IntegerField(name="sum", verbose_name="产品数量", help_text="当前项需要的产品数量")
    completed = models.IntegerField(name="completed",default=0, null=True, blank=True, verbose_name="完成数量", help_text="当前项已完成的数量")
    batch = models.CharField(max_length=32, null=True, blank=True, name="batch", verbose_name="产品批次", help_text="当前产品的批次")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间",help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间")
    create_user = models.CharField(max_length=32, name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.product_code + "  >>  " + self.product_name)


    class Meta:
        db_table = "ProductManagePlanItemModel"
        app_label = 'plan'
        verbose_name = "计划管理－产品管理计划子项"
        verbose_name_plural = verbose_name

class ProductManagePlanModel(models.Model):
    """
    产品管理计划
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("挂起", "挂起"),
        ("终止", "终止"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    PRIORITY = (
        ("正常", "正常"),
        ("优先", "优先"),
        ("紧急", "紧急"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="产品管理计划(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="产品管理计划(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的状态")
    priority = models.CharField(max_length=16, choices=PRIORITY, default="正常", name="priority", verbose_name="优先级",
                             help_text="当前信息的优先级")
    child = models.ManyToManyField(ProductManagePlanItemModel, blank=True, name="child",related_name="productManageItem_parent" , verbose_name="产品管理计划子项",help_text="当前产品管理计划子项")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="执行时间",help_text="当前任务执行的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", help_text="当前操作的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ProductManagePlanModel"
        app_label = 'plan'
        verbose_name = "计划管理－产品管理计划"
        verbose_name_plural = verbose_name
        permissions = {("read_productmanageplanmodel", u"Can read 计划管理－产品管理计划"),
                       ("admin_productmanageplanmodel", u"Can admin 计划管理－产品管理计划"),
                       ("deal_productmanageplanmodel", u"Can deal 计划管理－产品管理计划")}


class EquipmentMaintainPlanItemModel(models.Model):
    """
    设备维护计划子项
    """
    STATUS = (
        ("新建", "新建"),
        ("等待", "等待"),
        ("终止", "终止"),
        ("完成", "完成")
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    equipmentType_code = models.CharField(max_length=32, name="equipmentType_code",verbose_name="设备类型编码", help_text="当前维修记录对应的设备类型编码")
    equipmentType_name = models.CharField(max_length=32, name="equipmentType_name",verbose_name="设备类型名称", help_text="当前维修记录对应的设备类型名称")
    equipment_id = models.CharField(max_length=32, name="equipment_id",verbose_name="设备id", help_text="当前维修记录对应的设备id")
    equipment_code = models.CharField(max_length=32, name="equipment_code",verbose_name="设备编码", help_text="当前维修记录对应的设备编码")
    equipment_name = models.CharField(max_length=32, name="equipment_name",verbose_name="设备名称", help_text="当前维修记录对应的设备名称")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", help_text="当前维护计划的文件信息")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    handler = models.CharField(max_length=32, name="handler",null=True, blank=True, verbose_name="操作者", help_text="进行维护的人员是")
    consuming_time=models.CharField(max_length=32, name="consuming_time", verbose_name="计划维护耗时", help_text="进行此次维护计划的消耗的时间")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = "EquipmentMaintainPlanItemModel"
        app_label = 'plan'
        verbose_name = "计划管理－设备维护计划子项"
        verbose_name_plural = verbose_name

class EquipmentMaintainPlanModel(models.Model):
    """
    设备维护计划
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中","使用中"),
        ("挂起", "挂起"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="计划名称(建议唯一)")
    code = models.CharField(max_length=32,unique=True, name="code", verbose_name="编码", help_text="设备维护计划编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="设备维护信息的使用状态")
    child = models.ManyToManyField(EquipmentMaintainPlanItemModel, blank=True, name="child", verbose_name="设备维护计划子项",
                                  help_text="当前设备维护计划子项")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="维修时间",help_text="当前设备维修的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", help_text="当前维护计划的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "EquipmentMaintainPlanModel"
        app_label = 'plan'
        verbose_name = "计划管理－设备维护计划"
        verbose_name_plural = verbose_name
        permissions = {("read_equipmentmaintainplanmodel", u"Can read 计划管理－设备维护计划"),
                       ("admin_equipmentmaintainplanmodel", u"Can admin 计划管理－设备维护计划"),
                       ("deal_equipmentmaintainplanmodel", u"Can deal 计划管理－设备维护计划")}

class PlanBoardModel(models.Model):
    """
    计划看板定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="计划看板名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",help_text="计划看板编号(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的使用状态")
    image = models.ForeignKey(PlanImageModel, on_delete=models.CASCADE, name="image",  verbose_name="缩略图", help_text="当前看板的缩略图")
    file = models.ManyToManyField(PlanFileModel, blank=True, name="file", verbose_name="文件", help_text="当前看板的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(PlanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'PlanBoardModel'
        app_label = "plan"
        verbose_name = "计划管理－计划看板定义"
        verbose_name_plural = verbose_name
        permissions = {("read_planboardmodel", u"Can read 计划管理－计划看板定义"),
                       ("admin_planboardmodel", u"Can admin 计划管理－计划看板定义")}