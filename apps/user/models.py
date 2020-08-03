from django.contrib.auth.models import AbstractUser
from django.db import models

class UserAuditRecordModel(models.Model):
    """
     当前APP所有的操作日志
    """
    id = models.AutoField(primary_key=True, unique=True)
    uri = models.CharField(max_length=32, null=True, blank=True, name="uri", verbose_name="资源名称",help_text="当前操作的资源名称")
    uri_id = models.CharField(max_length=16, null=True, blank=True, name="uri_id", verbose_name="资源索引", help_text="当前操作的资源索引项")
    time = models.DateTimeField(auto_now_add=True, verbose_name="时间", help_text="进行操作的时间")
    classes = models.CharField(max_length=16, null=True, blank=True, name="classes", verbose_name="类别",help_text="进行操作的类别")
    user = models.CharField(max_length=16, null=True, blank=True, name="user",verbose_name="账号", help_text="进行操作的账号名称")
    result = models.CharField(max_length=16, null=True, blank=True, name="result", verbose_name="结果", help_text="进行操作的结果")
    content = models.TextField(null=True, blank=True, name="content", verbose_name="内容", help_text="进行当前操作具体涉及哪些内容")

    def __str__(self):
        return (self.uri + "  >>  "+ self.uri_id)

    class Meta:
        db_table = "UserAuditRecordModel"
        app_label = 'user'
        verbose_name = "账号管理---操作记录"
        verbose_name_plural = verbose_name
        permissions = {("read_userauditrecordmodel", u"Can read 账号管理---操作记录")}


class UserInforModel(AbstractUser):
    """
     用户信息表
    """
    job_number = models.CharField(max_length=20, null=True, blank=True, name="job_number", verbose_name="工号", help_text="当前用户的工号")
    post = models.CharField(max_length=20, null=True, blank=True, name="post", verbose_name="职位", help_text="当前用户的职位" )
    wechat = models.CharField(max_length=16, null=True, blank=True, name="wechat", verbose_name="微信", help_text="当前用户的微信" )
    mobile = models.CharField(max_length=11,null=True, blank=True,  verbose_name="手机", help_text="当前用户的手机号码")
    image = models.ImageField(null=True, blank=True,upload_to="user/image/", name="image", verbose_name="照片", help_text="当前用户的照片")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    auditor = models.CharField(max_length=16,  name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前用户的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="更改当前用户信息的时间")

    class Meta:
        db_table = "UserInforModel"
        app_label = 'user'
        verbose_name = "账号管理---账号信息"
        verbose_name_plural = verbose_name
        permissions = {("read_userinformodel", u"Can read 账号管理---账号信息"),
                       ("admin_userinformodel", u"Can admin 账号管理---账号信息")}


