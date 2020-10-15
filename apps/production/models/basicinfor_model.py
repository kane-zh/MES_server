from django.db import models

class ProductionAuditRecordModel(models.Model):
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
        db_table = "ProductionAuditRecordModel"
        app_label = 'production'
        verbose_name = "生产管理－操作记录"
        verbose_name_plural = verbose_name
        permissions={("read_productionauditrecordmodel", u"Can read 生产管理－操作记录")}

class ProductionAlterRecordModel(models.Model):
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
        db_table = "ProductionAlterRecordModel"
        app_label = 'production'
        verbose_name = "生产管理－审核记录"
        verbose_name_plural = verbose_name

class ProductionImageModel(models.Model):
    """
     当前APP所有的图片项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="production/image/", help_text="当前APP照片")
    image_name=models.CharField(max_length=32,name="image_name", null=True, blank=True, verbose_name="照片名", help_text="当前图片的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前图片属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user",  verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
      return (self.uri+"  >>  "+self.image_name)

    class Meta:
        db_table = "ProductionImageModel"
        app_label = 'production'
        verbose_name = "生产管理－图片项"
        verbose_name_plural = verbose_name

class ProductionFileModel(models.Model):
    """
    当前APP所有的文件项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    file = models.FileField(upload_to="production/file/", help_text="当前APP文件")
    file_name = models.CharField(max_length=32, name="file_name", null=True, blank=True, verbose_name="文件名", help_text="当前文件的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前文件属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.uri+"  >>  "+self.file_name)

    class Meta:
        db_table = "ProductionFileModel"
        app_label = 'production'
        verbose_name = "生产管理－文件项"
        verbose_name_plural = verbose_name

class WorkshopInforDefinitionModel(models.Model):
    """
    车间信息定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称",help_text="车间名称(建议唯一)")
    code = models.CharField(max_length=32,unique=True, name="code", verbose_name="编码", help_text="车间编码(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="车间信息的使用状态")
    classes = models.CharField(max_length=16,choices=CLASS, name="classes", verbose_name="类别", help_text="当前车间处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, name="parent",verbose_name="父类别", 
                               related_name="workshopInfor_child", help_text="当前车间的上一层级")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片", help_text="当前车间的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件", help_text="当前车间的文件信息")
    affiliation = models.CharField(max_length=32, null=True, blank=True, name="affiliation", verbose_name="归属单位",
                                   help_text="当前车间归属于那个公司/部门")
    location = models.CharField(max_length=32, null=True, blank=True, name="location", verbose_name="地理位置", help_text="当前车间所在的地理位置(地址)")
    principal = models.CharField(max_length=32, null=True, blank=True, name="principal", verbose_name="责任人",help_text="当前车间的责任人是谁")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="班组附加属性",help_text="当前车间下班组的附加属性")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=16,  name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32,name="auditor", verbose_name="审核账号",help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录", help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "WorkshopInforDefinitionModel"
        app_label = 'production'
        verbose_name = "生产管理－车间信息定义"
        verbose_name_plural = verbose_name
        permissions = {("read_workshopinfordefinitionmodel", u"Can read 生产管理－车间信息定义"),
                       ("admin_workshopinfordefinitionmodel", u"Can admin 生产管理－车间信息定义")}

class TeamInforDefinitionModel(models.Model):
    """
    班组信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="班组名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码",help_text="班组编号((与类型联合唯一))")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="班组信息的使用状态")
    type = models.ForeignKey(WorkshopInforDefinitionModel,on_delete=models.CASCADE,name="type", verbose_name="归属车间",
                               related_name="workshopInfor_item",help_text="当前班组归属于的车间")
    principal = models.CharField(max_length=32, null=True, blank=True, name="principal", verbose_name="责任人",help_text="当前班组的责任人是谁")
    duties = models.TextField( null=True, blank=True, name="duties", verbose_name="职责", help_text="当前班组的主要职责")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前班组的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前班组的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前班组的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前班组的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前班组的属性5")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片", help_text="当前班组的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件",help_text="当前班组的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注", help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")

    create_user = models.CharField(max_length=16,name="create_user",verbose_name="创建账号",help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor",verbose_name="审核账号",help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = "TeamInforDefinitionModel"
        app_label = 'production'
        verbose_name = "生产管理－班组信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_teaminfordefinitionmodel", u"Can read 生产管理－班组信息定义"),
                       ("admin_teaminfordefinitionmodel", u"Can admin 生产管理－班组信息定义")}


class SkillTypeDefinitionModel(models.Model):
    """
    技能类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="技能类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="技能类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="技能类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="skillType_child",on_delete=models.CASCADE, help_text="当前技能类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="技能附加属性",
                                        help_text="当前技能类型下技能的附加属性")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="技能类型文件",
                                  help_text="当前技能类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SkillTypeDefinitionModel"
        app_label = 'production'
        verbose_name = "生产管理－技能类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_skilltypedefinitionmodel", u"Can read 生产管理－技能类型定义"),
                       ("admin_skilltypedefinitionmodel", u"Can admin 生产管理－技能类型定义")}

class SkillInforDefinitionModel(models.Model):
    """
    技能信息定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="技能(内部)名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", verbose_name="编码", help_text="技能编号((与类型联合唯一))")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前技能信息的使用状态")
    type = models.ForeignKey(SkillTypeDefinitionModel, on_delete=models.CASCADE, name="type", related_name="skillType_item",
                             verbose_name="类型", help_text="当前技能属于的技能类型")
    rule = models.TextField(null=True, blank=True, name="rule", verbose_name="评定规则", help_text="此技能的评定规则是什么")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片",help_text="当前技能的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件",help_text="当前技能的文件信息")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前技能附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前技能附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前技能附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前技能附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前技能附加的属性5")
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
        db_table = 'SkillInforDefinitionModel'
        app_label = "production"
        verbose_name = "生产管理－技能信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'type')
        permissions = {("read_skillinfordefinitionmodel", u"Can read 生产管理－技能信息定义"),
                       ("admin_skillinfordefinitionmodel", u"Can admin 生产管理－技能信息定义")}

class PersonnelInforDefinitionModel(models.Model):
    """
    人员信息定义
    """
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="人员名称(建议唯一)")
    code = models.CharField(max_length=32, name="code",unique=True, verbose_name="编码",help_text="人员编号(与班组联合唯一)")
    workshop_code = models.CharField(max_length=32, name="workshop_code", verbose_name="车间编码", help_text="当前人员关联的车间编码")
    workshop_name = models.CharField(max_length=32, name="workshop_name", verbose_name="车间名称", help_text="当前人员关联的车间名称")
    team = models.ForeignKey(TeamInforDefinitionModel, on_delete=models.CASCADE,name="team", related_name="team_personnel",
                             verbose_name="从属班组", help_text="当前人员属于的班组")
    skill = models.ManyToManyField(SkillInforDefinitionModel, blank=True, name="skill", related_name="skill_personnel",
                                   verbose_name="技能",help_text="当前人员具有的技能")
    job_number = models.CharField(max_length=32, null=True, blank=True, name="job_number", verbose_name="工号", help_text="当前人员的工号")
    post = models.CharField(max_length=32, null=True, blank=True, name="post", verbose_name="职位", help_text="当前人员的职位" )
    wechat = models.CharField(max_length=32, null=True, blank=True, name="wechat", verbose_name="微信", help_text="当前人员的微信" )
    mobile = models.CharField(max_length=11,null=True, blank=True,  verbose_name="手机", help_text="当前用户的手机号码")
    image = models.ManyToManyField(ProductionImageModel, blank=True, name="image", verbose_name="照片",help_text="当前人员的照片信息")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件", help_text="当前人员的文件信息")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前人员附加的属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前人员附加的属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前人员附加的属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前人员附加的属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前人员附加的属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'PersonnelInforDefinitionModel'
        app_label = "production"
        verbose_name = "生产管理－人员信息定义"
        verbose_name_plural = verbose_name
        unique_together = ('code', 'team')
        permissions = {("read_personnelinfordefinitionmodel", u"Can read 生产管理－人员信息定义"),
                       ("admin_personnelinfordefinitionmodel", u"Can admin 生产管理－人员信息定义")}


class AssessmentTypeDefinitionModel(models.Model):
    """
    考核类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="考核类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="考核类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="考核类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="assessmentType_child", on_delete=models.CASCADE, help_text="当前考核类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="考核附加属性",
                                        help_text="当前考核类型下考核的附加属性")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="考核类型文件",
                                  help_text="当前考核类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "AssessmentTypeDefinitionModel"
        app_label = 'production'
        verbose_name = "生产管理－考核类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_assessmenttypedefinitionmodel", u"Can read 生产管理－考核类型定义"),
                       ("admin_assessmenttypedefinitionmodel", u"Can admin 生产管理－考核类型定义")}

class AssessmentLevelDefinitionModel(models.Model):
    """
    考核等级定义
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
    rule = models.TextField(null=True, blank=True, name="rule", verbose_name="评定规则",help_text="此考核等级的评定规则是什么")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="产品文件",help_text="当前考核等级的文件信息")
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
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "AssessmentLevelDefinitionModel"
        app_label = 'production'
        verbose_name = "生产管理－考核等级定义"
        verbose_name_plural = verbose_name
        permissions = {("read_assessmentleveldefinitionModel", u"Can read 生产管理－考核等级定义"),
                       ("admin_assessmentleveldefinitionModel", u"Can admin 生产管理－考核等级定义")}
class ProductDataTypeDefinitionModel(models.Model):
    """
    产品过程数据类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="产品过程数据类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="产品过程数据类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="产品过程数据类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="productDataType_child", on_delete=models.CASCADE, help_text="当前产品过程数据类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="产品过程数据附加属性",
                                        help_text="当前产品过程数据类型下产品过程数据的附加属性")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="产品过程数据类型文件",
                                  help_text="当前产品过程数据类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ProductDataTypeDefinitionModel"
        app_label = 'production'
        verbose_name = "生产管理－产品过程数据类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_productdatatypedefinitionmodel", u"Can read 生产管理－产品过程数据类型定义"),
                       ("admin_productdatatypedefinitionmodel", u"Can admin 生产管理－产品过程数据类型定义")}


class SemifinishedDataTypeDefinitionModel(models.Model):
    """
    半成品过程数据类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="半成品过程数据类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="半成品过程数据类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="半成品过程数据类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="semifinishedDataType_child", on_delete=models.CASCADE, help_text="当前半成品过程数据类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="半成品过程数据附加属性",
                                        help_text="当前半成品过程数据类型下半成品过程数据的附加属性")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="半成品过程数据类型文件",
                                  help_text="当前半成品过程数据类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SemifinishedDataTypeDefinitionModel"
        app_label = 'production'
        verbose_name = "生产管理－半成品过程数据类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_semifinisheddatatypedefinitionmodel", u"Can read 生产管理－半成品过程数据类型定义"),
                       ("admin_semifinisheddatatypedefinitionmodel", u"Can admin 生产管理－半成品过程数据类型定义")}

class EventTypeDefinitionModel(models.Model):
    """
    事件类型定义
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
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="事件类型名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", unique=True, verbose_name="编码", help_text="事件类型编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    classes = models.CharField(max_length=16, choices=CLASS, name="classes", verbose_name="类别", help_text="事件类型处于的层级类别")
    parent = models.ForeignKey("self", null=True, blank=True, name="parent", verbose_name="父类别",
                               related_name="eventType_child", on_delete=models.CASCADE, help_text="当前事件类型属于的上一级别")
    attach_attribute = models.TextField(null=True, blank=True, name="attach_attribute", verbose_name="事件附加属性",
                                        help_text="当前事件类型下事件的附加属性")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="事件类型文件",
                                  help_text="当前事件类型的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(ProductionAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "EventTypeDefinitionModel"
        app_label = 'production'
        verbose_name = "生产管理－事件类型定义"
        verbose_name_plural = verbose_name
        permissions = {("read_eventtypedefinitionmodel", u"Can read 生产管理－事件类型定义"),
                       ("admin_eventtypedefinitionmodel", u"Can admin 生产管理－事件类型定义")}
class ProductionBoardModel(models.Model):
    """
    生产看板定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="生产看板名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",help_text="生产看板编号(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的使用状态")
    image = models.ForeignKey(ProductionImageModel, on_delete=models.CASCADE, name="image",  verbose_name="缩略图", help_text="当前看板的缩略图")
    file = models.ManyToManyField(ProductionFileModel, blank=True, name="file", verbose_name="文件", help_text="当前看板的文件信息")
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
        db_table = 'ProductionBoardModel'
        app_label = "production"
        verbose_name = "生产管理－生产看板定义"
        verbose_name_plural = verbose_name
        permissions = {("read_productionboardmodel", u"Can read 生产管理－生产看板定义"),
                       ("admin_productionboardmodel", u"Can admin 生产管理－生产看板定义")}