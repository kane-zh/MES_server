from rest_framework import serializers
from apps.lean.models.basicinfor_model import *
from commonFunction import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()

# region  当前APP操作记录 序列化器
class LeanAuditRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP操作记录---list
    """
    class Meta:
        model = LeanAuditRecordModel
        fields = ("id", "uri", "uri_id", "time","classes", "user","result")

class LeanAuditRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    当前APP操作记录---retrieve
    """
    class Meta:
        model = LeanAuditRecordModel
        fields = "__all__"

# endregion

# region  当前APP审核记录 序列化器
class LeanAlterRecordSerialize_Create(serializers.ModelSerializer):
    """
    当前APP审核记录--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LeanAlterRecordModel
        fields = ("id", "uri", "desc","create_user", )

class LeanAlterRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP审核记录---list
    """
    class Meta:
        model = LeanAlterRecordModel
        fields = "__all__"

# endregion

# region  当前APP文件/图片  序列化器
class LeanImageSerialize_Create(serializers.ModelSerializer):
    """
    当前APP图片--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LeanImageModel
        fields = ("id", "image", "uri", "desc","create_user")

    def validate(self, attrs):
        attrs["image_name"]=attrs["image"]
        return attrs

class LeanImageSerialize_List(serializers.ModelSerializer):
    """
    当前APP图片--list
    """
    class Meta:
        model = LeanImageModel
        fields =  "__all__"

class LeanFileSerialize_Create(serializers.ModelSerializer):
    """
    当前APP文件--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LeanFileModel
        fields = ("id", "file", "uri", "desc", "create_user")

    def validate(self, attrs):
        attrs["file_name"] = attrs["file"]
        return attrs

class LeanFileSerialize_List(serializers.ModelSerializer):
    """
    当前APP文件--list
    """
    class Meta:
        model = LeanFileModel
        fields =  "__all__"

# endregion

# region  精益看板定义  序列化器
class LeanBoardSerialize_Create(serializers.ModelSerializer):

    """
    精益看板定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LeanBoardModel
        fields = ("id", "name", "code","state", "image", "file","desc", "auditor","create_user"
                  )
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('lean.add_leanboardmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        return  attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('lean.admin_leanboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class  LeanBoardSerialize_List(serializers.ModelSerializer):

    """
    精益看板定义--list
    """
    image = LeanImageSerialize_List()
    class Meta:
        model = LeanBoardModel
        fields = ("id", "name", "code", "state","image","create_user","auditor","create_time","update_time")


class LeanBoardSerialize_Retrieve(serializers.ModelSerializer):

    """
    精益看板定义--retrieve
    """
    image = LeanImageSerialize_List()
    file =LeanFileSerialize_List(many=True)
    alter = LeanAlterRecordSerialize_List(many=True)

    class Meta:
        model = LeanBoardModel
        fields = "__all__"


class LeanBoardSerialize_Update(serializers.ModelSerializer):
    """
    精益看板定义--update
    """

    class Meta:
        model = LeanBoardModel
        fields = ("id", "name", "code", "image", "file","desc", "auditor")

     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return  attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True:
            if self.instance.create_user == value:  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('lean.admin_leanboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class LeanBoardSerialize_Partial(serializers.ModelSerializer):
    """
    精益看板定义--partial
    """

    class Meta:
        model = LeanBoardModel
        fields = ("id", "state", "alter")

    # 所有字段验证
    def validate(self, attrs):
        try:
            del attrs['alter']  # 删除alter字段
        except Exception:
            pass
        return attrs

    # 状态字段验证
    def validate_state(self, value):
        validate_states(self.instance.state, value)
        if ((self.instance.create_user == self.context['request'].user.username) and\
             (self.instance.auditor != self.context['request'].user.username)):   # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = LeanBoardModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion