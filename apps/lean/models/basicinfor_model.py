from django.db import models

class LeanAuditRecordModel(models.Model):
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
        db_table = "LeanAuditRecordModel"
        app_label = 'lean'
        verbose_name = "精益管理－操作记录"
        verbose_name_plural = verbose_name
        permissions={("read_leanauditrecordmodel", u"Can read 精益管理－操作记录")}

class LeanAlterRecordModel(models.Model):
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
        db_table = "LeanAlterRecordModel"
        app_label = 'lean'
        verbose_name = "精益管理－审核记录"
        verbose_name_plural = verbose_name

class LeanImageModel(models.Model):
    """
     当前APP所有的图片项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    image = models.ImageField(upload_to="lean/image/", help_text="当前APP照片")
    image_name=models.CharField(max_length=32,name="image_name", null=True, blank=True, verbose_name="照片名", help_text="当前图片的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前图片属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user",  verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
      return (self.uri+"  >>  "+self.image_name)

    class Meta:
        db_table = "LeanImageModel"
        app_label = 'lean'
        verbose_name = "精益管理－图片项"
        verbose_name_plural = verbose_name

class LeanFileModel(models.Model):
    """
    当前APP所有的文件项保存
    """
    id = models.AutoField(primary_key=True, unique=True)
    file = models.FileField(upload_to="lean/file/", help_text="当前APP文件")
    file_name = models.CharField(max_length=32, name="file_name", null=True, blank=True, verbose_name="文件名", help_text="当前文件的名称")
    uri = models.CharField(max_length=32,name="uri", null=True, blank=True, verbose_name="资源名",help_text="当前文件属于资源的名称")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return (self.uri+"  >>  "+self.file_name)

    class Meta:
        db_table = "LeanFileModel"
        app_label = 'lean'
        verbose_name = "精益管理－文件项"
        verbose_name_plural = verbose_name

class LeanBoardModel(models.Model):
    """
    精益看板定义
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称", help_text="精益看板名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码",help_text="精益看板编号(必须唯一)")
    state = models.CharField(max_length=16,choices=STATUS, default="新建", name="state", verbose_name="状态",help_text="当前信息的使用状态")
    image = models.ForeignKey(LeanImageModel, on_delete=models.CASCADE, name="image",  verbose_name="缩略图", help_text="当前看板的缩略图")
    file = models.ManyToManyField(LeanFileModel, blank=True, name="file", verbose_name="文件", help_text="当前看板的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(LeanAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = 'LeanBoardModel'
        app_label = "lean"
        verbose_name = "精益管理－精益看板定义"
        verbose_name_plural = verbose_name
        permissions = {("read_leanboardmodel", u"Can read 精益管理－精益看板定义"),
                       ("admin_leanboardmodel", u"Can admin 精益管理－精益看板定义")}