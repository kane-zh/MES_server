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
# region 事件类型定义 序列化器
class EventTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    事件类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EventTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('lean.add_eventtypedefinitionmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('lean.admin_eventtypedefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 父类别字段验证
    def validate_parent(self, value):
        if self.initial_data['classes'] == "一级类别":  # 判断 类别是否为一级类别
            if value != None:  # 一级类别不能指定父类别
                raise serializers.ValidationError("处于[一级类别]的信息不能指定父类别")
        else:
            if value is None:  # 非一级类别必须指定父类别
                raise serializers.ValidationError("处于" + self.initial_data["classes"] + "类别的信息必须指定父类别")
            else:  # 判断指定的父类别是否符合条件
                list = EventTypeDefinitionModel.objects.get(id=value.id)
                if list is None:  # 判断 父类别是否存在
                    raise serializers.ValidationError("指定的父类别不存在")
                elif (list.state != "使用中"):  # 判断 父类别状态是否合适
                    raise serializers.ValidationError("指定的父类别不在--'使用中'状态")
                else:  # 判断  子父类别的层级是否合适
                    if self.initial_data['classes'] == "二级类别" and list.classes != "一级类别":
                        raise serializers.ValidationError("[二级类别]的父类别必须是[一级类别]'")
                    if self.initial_data['classes'] == "三级类别" and list.classes != "二级类别":
                        raise serializers.ValidationError("[三级类别]的父类别必须是[二级类别]")
                    if self.initial_data['classes'] == "四级类别" and list.classes != "三级类别":
                        raise serializers.ValidationError("[四级类别]的父类别必须是[三级类别]")
        return value


class EventTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    事件类型定义--list
    """
    class Meta:
        model = EventTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class EventInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    事件定义--事件类型定义
    """

    class Meta:
        model = EventInforDefinitionModel
        fields = ("id", "topic","state", "content",  "result", "create_user")

class EventTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    事件类型定义--retrieve
    """
    file = LeanFileSerialize_List(many=True)                 # 类型文件信息
    alter = LeanAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = EventTypeDefinitionSerialize_List(required=False)   # 父类别信息
    eventType_child = EventTypeDefinitionSerialize_List(many=True)# 子类别信息
    eventType_item = EventInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = EventTypeDefinitionModel
        fields = "__all__"


class EventTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    事件类型定义--update
    """
    class Meta:
        model = EventTypeDefinitionModel
        fields = ("id", "name", "code", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor",)

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True:
            if self.instance.create_user == value:  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('lean.admin_eventtypedefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 父类别字段验证
    def validate_parent(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if self.initial_data['classes'] == "一级类别":  # 判断 类别是否为一级类别
            if value != None:  # 一级类别不能指定父类别
                raise serializers.ValidationError("处于[一级类别]的信息不能指定父类别")
        else:
            if value is None:  # 非一级类别必须指定父类别
                raise serializers.ValidationError("处于" + self.initial_data["classes"] + "类别的信息必须指定父类别")
            else:  # 判断指定的父类别是否符合条件
                list = EventTypeDefinitionModel.objects.get(id=value.id)
                if list is None:  # 判断 父类别是否存在
                    raise serializers.ValidationError("指定的父类别不存在")
                elif (list.state != "使用中"):  # 判断 父类别状态是否合适
                    raise serializers.ValidationError("指定的父类别不在--'使用状态'")
                else:  # 判断  子父类别的层级是否合适
                    if self.initial_data['classes'] == "二级类别" and list.classes != "一级类别":
                        raise serializers.ValidationError("[二级类别]的父类别必须是[一级类别]'")
                    if self.initial_data['classes'] == "三级类别" and list.classes != "二级类别":
                        raise serializers.ValidationError("[三级类别]的父类别必须是[二级类别]")
                    if self.initial_data['classes'] == "四级类别" and list.classes != "三级类别":
                        raise serializers.ValidationError("[四级类别]的父类别必须是[三级类别]")
        return value


class EventTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    事件类型定义--partial
    """
    class Meta:
        model = EventTypeDefinitionModel
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
        obj = EventTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 事件类型层级结构 序列化器
class EventTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    事件类型层级结构--fourth
    """
    class Meta:
        model = EventTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class EventTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    事件类型定义--third
    """
    eventType_child = EventTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = EventTypeDefinitionModel
        fields = ("id", "name", "code", "state", "eventType_child")

class EventTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    事件类型定义--second
    """
    eventType_child = EventTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = EventTypeDefinitionModel
        fields = ("id", "name", "code", "state", "eventType_child")

class EventTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    事件类型定义--fitst
    """
    eventType_child = EventTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = EventTypeDefinitionModel
        fields = ("id", "name", "code", "state","eventType_child")

# endregion

# region  事件信息定义  序列化器
class EventInforDefinitionSerialize_Create(serializers.ModelSerializer):

    """
    事件信息定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EventInforDefinitionModel
        fields = ("id", "topic","state","type", "image", "file","content","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",  "desc","create_user")
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_eventinfordefinitionmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        return  attrs

    # 类型字段验证
    def validate_type(self, value):
        list = EventTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class EventInforDefinitionSerialize_List(serializers.ModelSerializer):

    """
    事件信息定义--list
    """
    type = EventTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = EventInforDefinitionModel
        fields = ("id", "topic","state","type","content","result","attribute1", "attribute2","attribute3", "attribute4","attribute5", "update_time","create_user"
                  )


class EventInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):

    """
    事件信息定义--retrieve
    """
    image = LeanImageSerialize_List(many=True)
    file = LeanFileSerialize_List(many=True)
    type = EventTypeDefinitionSerialize_List(required=False)

    class Meta:
        model = EventInforDefinitionModel
        fields = "__all__"


class EventInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    事件信息定义--update
    """

    class Meta:
        model = EventInforDefinitionModel
        fields = ("id", "topic","type", "image", "file","content","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc",)
     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return  attrs

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = EventTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class EventInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    事件信息定义--partial
    """
    class Meta:
        model = EventInforDefinitionModel
        fields = ("id", "state","result")

    # 状态字段验证
    def validate_state(self, value):
        if (self.instance.state == "新建" and \
                (value == "发布" or value == "作废")):
            return value
        if (self.instance.state == "发布" and \
                (value == "完成" or value == "作废")):
            return value
        if (self.instance.state == "完成" and \
                (value == "作废")):
            return value
        raise serializers.ValidationError("不能从" + self.instance.state + "更新到" + value)
        return value
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