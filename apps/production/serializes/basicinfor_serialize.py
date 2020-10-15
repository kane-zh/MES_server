from rest_framework import serializers
from apps.production.models.basicinfor_model import *
from apps.production.models.recording_model import *
from commonFunction import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()

# region  当前APP操作记录 序列化器
class ProductionAuditRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP操作记录---list
    """
    class Meta:
        model = ProductionAuditRecordModel
        fields = ("id", "uri", "uri_id", "time","classes", "user","result")

class ProductionAuditRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    当前APP操作记录---retrieve
    """
    class Meta:
        model = ProductionAuditRecordModel
        fields = "__all__"

# endregion

# region  当前APP审核记录 序列化器
class ProductionAlterRecordSerialize_Create(serializers.ModelSerializer):
    """
    当前APP审核记录--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductionAlterRecordModel
        fields = ("id", "uri", "desc","create_user", )

class ProductionAlterRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP审核记录---list
    """
    class Meta:
        model = ProductionAlterRecordModel
        fields = "__all__"

# endregion

# region  当前APP文件/图片  序列化器
class ProductionImageSerialize_Create(serializers.ModelSerializer):
    """
    当前APP图片--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductionImageModel
        fields = ("id", "image", "uri", "desc","create_user")

    def validate(self, attrs):
        attrs["image_name"]=attrs["image"]
        return attrs

class ProductionImageSerialize_List(serializers.ModelSerializer):
    """
    当前APP图片--list
    """
    class Meta:
        model = ProductionImageModel
        fields =  "__all__"

class ProductionFileSerialize_Create(serializers.ModelSerializer):
    """
    当前APP文件--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductionFileModel
        fields = ("id", "file", "uri", "desc", "create_user")

    def validate(self, attrs):
        attrs["file_name"] = attrs["file"]
        return attrs

class ProductionFileSerialize_List(serializers.ModelSerializer):
    """
    当前APP文件--list
    """
    class Meta:
        model = ProductionFileModel
        fields =  "__all__"

# endregion

# region 车间信息定义 序列化器
class WorkshopInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    车间信息定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WorkshopInforDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent","image", "file",
                  "affiliation", "location", "principal","attach_attribute","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_workshopinfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_workshopinfordefinitionmodel'):
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
                list = WorkshopInforDefinitionModel.objects.get(id=value.id)
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


class WorkshopInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    车间信息定义--list
    """

    class Meta:
        model = WorkshopInforDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time","create_time","update_time")


class TeamInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    班组信息定义--车间信息定义
    """

    class Meta:
        model = TeamInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")


class WorkshopInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    车间信息定义--retrieve
    """
    file = ProductionFileSerialize_List(many=True)  # 类型文件信息
    image=ProductionImageSerialize_List(many=True)
    alter = ProductionAlterRecordSerialize_List(many=True)  # 审核记录信息
    parent = WorkshopInforDefinitionSerialize_List(required=False)  # 父类别信息
    workshopInfor_child = WorkshopInforDefinitionSerialize_List(many=True)  # 子类别信息
    workshopInfor_item = TeamInforDefinitionSerialize_Type(many=True)  # 附属项信息

    class Meta:
        model = WorkshopInforDefinitionModel
        fields = "__all__"


class WorkshopInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    车间信息定义--update
    """

    class Meta:
        model = WorkshopInforDefinitionModel
        fields = ("id", "name", "code", "classes", "parent", "image", "file",
                  "affiliation", "location", "principal","attach_attribute","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor",)

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
        if not auditor.has_perm('production.admin_workshopinfordefinitionmodel'):
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
                list = WorkshopInforDefinitionModel.objects.get(id=value.id)
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

class WorkshopInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    车间信息定义--partial
    """
    class Meta:
        model = WorkshopInforDefinitionModel
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
             (self.instance.auditor != self.context['request'].user.username)):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = WorkshopInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value


# endregion

# region 车间层级结构 序列化器
class WorkshopInforDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    车间层级结构--fourth
    """
    class Meta:
        model = WorkshopInforDefinitionModel
        fields = ("id", "name", "code", "state")

class WorkshopInforDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    车间层级结构--third
    """
    workshopInfor_child = WorkshopInforDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = WorkshopInforDefinitionModel
        fields = ("id", "name", "code", "state", "workshopInfor_child")

class WorkshopInforDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    车间层级结构--second
    """
    workshopInfor_child = WorkshopInforDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = WorkshopInforDefinitionModel
        fields = ("id", "name", "code", "state", "workshopInfor_child")

class WorkshopInforDefinitionSerialize_First(serializers.ModelSerializer):
    """
    车间层级结构--fitst
    """
    workshopInfor_child = WorkshopInforDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = WorkshopInforDefinitionModel
        fields = ("id", "name", "code", "state","workshopInfor_child")

# endregion

# region 班组信息定义 序列化器
class TeamInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    班组信息定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TeamInforDefinitionModel
        fields = ("id", "name", "code", "state","type","principal","duties",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "image", "file","desc", "auditor", "create_user"
                  )

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_teaminfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_teaminfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = WorkshopInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value



class TeamInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    班组信息定义--list
    """
    type = WorkshopInforDefinitionSerialize_List(required=False)
    class Meta:
        model = TeamInforDefinitionModel
        fields = ("id", "name", "code", "state","type", "principal", "duties", "desc", "auditor", "create_user",
                  "create_time","update_time")
class PersonnelInforDefinitionSerialize_team(serializers.ModelSerializer):
    """
    人员信息定义--班组信息定义
    """
    class Meta:
        model = PersonnelInforDefinitionModel
        fields = ("id", "name", "code","job_number","post","wechat","mobile", "create_user"
                  ,"create_time","update_time")

class TeamInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    班组信息定义--retrieve
    """
    image =ProductionImageSerialize_List(many=True)
    file =ProductionFileSerialize_List(many=True)
    alter =ProductionAlterRecordSerialize_List(many=True)
    type = WorkshopInforDefinitionSerialize_List(required=False)
    team_personnel=PersonnelInforDefinitionSerialize_team(many=True)
    class Meta:
        model = TeamInforDefinitionModel
        fields = "__all__"


class TeamInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    班组信息定义--update
    """

    class Meta:
        model = TeamInforDefinitionModel
        fields = ("id", "name", "code","type","principal","duties",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "image", "file","desc", "auditor",)
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
        if not auditor.has_perm('production.admin_teaminfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = WorkshopInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class TeamInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    班组信息定义--partial
    """

    class Meta:
        model = TeamInforDefinitionModel
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
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = TeamInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 技能类型定义 序列化器
class SkillTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    技能类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SkillTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_skilltypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_skilltypedefinitionmodel'):
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
                list = SkillTypeDefinitionModel.objects.get(id=value.id)
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


class SkillTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    技能类型定义--list
    """
    class Meta:
        model = SkillTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class SkillInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    技能定义--技能类型定义
    """

    class Meta:
        model = SkillInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class SkillTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    技能类型定义--retrieve
    """
    file = ProductionFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProductionAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = SkillTypeDefinitionSerialize_List(required=False)      # 父类别信息
    skillType_child = SkillTypeDefinitionSerialize_List(many=True)  # 子类别信息
    skillType_item = SkillInforDefinitionSerialize_Type(many=True)  # 附属项信息

    class Meta:
        model = SkillTypeDefinitionModel
        fields = "__all__"


class SkillTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    技能类型定义--update
    """
    class Meta:
        model = SkillTypeDefinitionModel
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
        if not auditor.has_perm('production.admin_skilltypedefinitionmodel'):
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
                list = SkillTypeDefinitionModel.objects.get(id=value.id)
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


class SkillTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    技能类型定义--partial
    """
    class Meta:
        model = SkillTypeDefinitionModel
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
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = SkillTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 技能类型层级结构 序列化器
class SkillTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    技能类型层级结构--fourth
    """
    class Meta:
        model = SkillTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class SkillTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    技能类型层级结构--third
    """
    skillType_child = SkillTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = SkillTypeDefinitionModel
        fields = ("id", "name", "code", "state", "skillType_child")

class SkillTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    技能类型层级结构--second
    """
    skillType_child = SkillTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = SkillTypeDefinitionModel
        fields = ("id", "name", "code", "state", "skillType_child")

class SkillTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    技能类型层级结构--fitst
    """
    skillType_child = SkillTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = SkillTypeDefinitionModel
        fields = ("id", "name", "code", "state","skillType_child")

# endregion

# region 技能信息定义 序列化器
class SkillInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    技能信息定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SkillInforDefinitionModel
        fields = ("id", "name", "code", "state","type","rule",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "image", "file","desc", "auditor", "create_user"
                  )

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_skillinfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_skillinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = SkillTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value



class SkillInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    技能信息定义--list
    """
    type = SkillTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = SkillInforDefinitionModel
        fields = ("id", "name", "code", "state","type","rule",  "desc", "auditor", "create_user","create_time","update_time"
                  )
class PersonnelInforDefinitionSerialize_Skill(serializers.ModelSerializer):
    """
    人员信息定义--技能信息定义
    """
    class Meta:
        model = PersonnelInforDefinitionModel
        fields = ("id", "name", "code","job_number","post","wechat","mobile", "create_user"
                  )

class SkillInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    技能信息定义--retrieve
    """
    image =ProductionImageSerialize_List(many=True)
    file =ProductionFileSerialize_List(many=True)
    alter =ProductionAlterRecordSerialize_List(many=True)
    type = SkillTypeDefinitionSerialize_List(required=False)
    skill_personnel=PersonnelInforDefinitionSerialize_Skill(many=True)

    class Meta:
        model = SkillInforDefinitionModel
        fields = "__all__"


class SkillInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    技能信息定义--update
    """

    class Meta:
        model = SkillInforDefinitionModel
        fields = ("id", "name", "code","type","rule","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",
                  "image", "file","desc", "auditor",)
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
        if not auditor.has_perm('production.admin_skillinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = SkillTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class SkillInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    技能信息定义--partial
    """

    class Meta:
        model = SkillInforDefinitionModel
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
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = SkillInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 人员信息定义 序列化器
class PersonnelInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    人员信息定义--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PersonnelInforDefinitionModel
        fields = ("id", "name", "code", "team", "skill","job_number","post","wechat","mobile",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "image", "file","desc", "create_user"
                  )

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_personnelinfordefinitionmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        attrs["workshop_code"] = attrs["team"].type.code  # 获取车间编码
        attrs["workshop_name"] = attrs["team"].type.name  # 获取车间名称
        return attrs

    # 班组字段验证
    def validate_team(self, value):
        list = TeamInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的班组不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的班组不在--'使用状态'")
        return value



class PersonnelInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    人员信息定义--list
    """
    team=TeamInforDefinitionSerialize_List(required=False)
    class Meta:
        model = PersonnelInforDefinitionModel
        fields = ("id", "name","team","workshop_code","workshop_name", "code","job_number","post","wechat","mobile", "create_user"
                  ,"create_time","update_time")


class PersonnelInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    人员信息定义--retrieve
    """
    image =ProductionImageSerialize_List(many=True)
    file =ProductionFileSerialize_List(many=True)
    skill =SkillInforDefinitionSerialize_List(many=True)
    team = TeamInforDefinitionSerialize_List(required=False)

    class Meta:
        model = PersonnelInforDefinitionModel
        fields = "__all__"


class PersonnelInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    人员信息定义--update
    """

    class Meta:
        model = PersonnelInforDefinitionModel
        fields = ("id", "name", "code", "team", "skill","job_number","post","wechat","mobile",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "image", "file","desc")

    # 所有字段验证
    def validate(self, attrs):
        attrs["workshop_code"] = attrs["team"].type.code  # 获取车间编码
        attrs["workshop_name"] = attrs["team"].type.name  # 获取车间名称
        return attrs
    # 班组字段验证
    def validate_team(self, value):
        list = TeamInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的班组不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的班组不在--'使用状态'")
        return value
# endregion

# region 考核等级定义 序列化器
class AssessmentLevelDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    考核等级定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AssessmentLevelDefinitionModel
        fields = ("id", "name", "code", "state","rule",
                   "file","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","desc", "auditor", "create_user"
                  )

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_assessmentleveldefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_assessmentleveldefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

class AssessmentLevelDefinitionSerialize_List(serializers.ModelSerializer):
    """
    考核等级定义--list
    """
    class Meta:
        model = AssessmentLevelDefinitionModel
        fields = ("id", "name", "code", "state", "rule",  "desc", "auditor", "create_user","create_time","update_time"
                  )

class AssessmentLevelDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    考核等级定义--retrieve
    """
    file =ProductionFileSerialize_List(many=True)
    alter =ProductionAlterRecordSerialize_List(many=True)

    class Meta:
        model = AssessmentLevelDefinitionModel
        fields = "__all__"


class AssessmentLevelDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    考核等级定义--update
    """

    class Meta:
        model = AssessmentLevelDefinitionModel
        fields = ("id", "name", "code", "rule",
                  "file","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor")
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
        if not auditor.has_perm('production.admin_assessmentleveldefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class AssessmentLevelDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    考核等级定义--partial
    """

    class Meta:
        model = AssessmentLevelDefinitionModel
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
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = AssessmentLevelDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 考核类型定义 序列化器
class AssessmentTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    考核类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AssessmentTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_assessmenttypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_assessmenttypedefinitionmodel'):
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
                list = AssessmentTypeDefinitionModel.objects.get(id=value.id)
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


class AssessmentTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    考核类型定义--list
    """
    class Meta:
        model = AssessmentTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class AssessmentInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    考核定义--考核类型定义
    """

    class Meta:
        model = AssessmentRecordModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class AssessmentTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    考核类型定义--retrieve
    """
    file = ProductionFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProductionAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = AssessmentTypeDefinitionSerialize_List(required=False)      # 父类别信息
    assessmentType_child = AssessmentTypeDefinitionSerialize_List(many=True)  # 子类别信息
    assessmentType_item = AssessmentInforDefinitionSerialize_Type(many=True)  # 附属项信息

    class Meta:
        model = AssessmentTypeDefinitionModel
        fields = "__all__"


class AssessmentTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    考核类型定义--update
    """
    class Meta:
        model = AssessmentTypeDefinitionModel
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
        if not auditor.has_perm('production.admin_assessmenttypedefinitionmodel'):
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
                list = AssessmentTypeDefinitionModel.objects.get(id=value.id)
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


class AssessmentTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    考核类型定义--partial
    """
    class Meta:
        model = AssessmentTypeDefinitionModel
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
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = AssessmentTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 考核类型层级结构 序列化器
class AssessmentTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    考核类型层级结构--fourth
    """
    class Meta:
        model = AssessmentTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class AssessmentTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    考核类型层级结构--third
    """
    assessmentType_child = AssessmentTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = AssessmentTypeDefinitionModel
        fields = ("id", "name", "code", "state", "assessmentType_child")

class AssessmentTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    考核类型层级结构--second
    """
    assessmentType_child = AssessmentTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = AssessmentTypeDefinitionModel
        fields = ("id", "name", "code", "state", "assessmentType_child")

class AssessmentTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    考核类型层级结构--fitst
    """
    assessmentType_child = AssessmentTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = AssessmentTypeDefinitionModel
        fields = ("id", "name", "code", "state","assessmentType_child")

# endregion

# region 产品过程数据类型定义 序列化器
class ProductDataTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    产品过程数据类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductDataTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_productDatatypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_productDatatypedefinitionmodel'):
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
                list = ProductDataTypeDefinitionModel.objects.get(id=value.id)
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


class ProductDataTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    产品过程数据类型定义--list
    """
    class Meta:
        model = ProductDataTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class ProductDataDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    产品过程数据定义--产品过程数据类型定义
    """

    class Meta:
        model = ProductDataDefinitionModel
        fields = ("id", "name", "code", "state", "create_user")

class ProductDataTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品过程数据类型定义--retrieve
    """
    file = ProductionFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProductionAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = ProductDataTypeDefinitionSerialize_List(required=False)      # 父类别信息
    productDataType_child = ProductDataTypeDefinitionSerialize_List(many=True)  # 子类别信息
    productDataType_item = ProductDataDefinitionSerialize_Type(many=True)  # 附属项信息

    class Meta:
        model = ProductDataTypeDefinitionModel
        fields = "__all__"


class ProductDataTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    产品过程数据类型定义--update
    """
    class Meta:
        model = ProductDataTypeDefinitionModel
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
        if not auditor.has_perm('production.admin_productDatatypedefinitionmodel'):
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
                list = ProductDataTypeDefinitionModel.objects.get(id=value.id)
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


class ProductDataTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    产品过程数据类型定义--partial
    """
    class Meta:
        model = ProductDataTypeDefinitionModel
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
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = ProductDataTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 产品过程数据类型层级结构 序列化器
class ProductDataTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    产品过程数据类型层级结构--fourth
    """
    class Meta:
        model = ProductDataTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class ProductDataTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    产品过程数据类型层级结构--third
    """
    productDataType_child = ProductDataTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = ProductDataTypeDefinitionModel
        fields = ("id", "name", "code", "state", "productDataType_child")

class ProductDataTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    产品过程数据类型层级结构--second
    """
    productDataType_child = ProductDataTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = ProductDataTypeDefinitionModel
        fields = ("id", "name", "code", "state", "productDataType_child")

class ProductDataTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    产品过程数据类型层级结构--fitst
    """
    productDataType_child = ProductDataTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = ProductDataTypeDefinitionModel
        fields = ("id", "name", "code", "state","productDataType_child")

# endregion

# region 半成品过程数据类型定义 序列化器
class SemifinishedDataTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    半成品过程数据类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedDataTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_semifinishedDatatypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_semifinishedDatatypedefinitionmodel'):
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
                list = SemifinishedDataTypeDefinitionModel.objects.get(id=value.id)
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


class SemifinishedDataTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    半成品过程数据类型定义--list
    """
    class Meta:
        model = SemifinishedDataTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class SemifinishedDataDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    半成品过程数据定义--半成品过程数据类型定义
    """

    class Meta:
        model = SemifinishedDataDefinitionModel
        fields = ("id", "name", "code", "state", "create_user")

class SemifinishedDataTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品过程数据类型定义--retrieve
    """
    file = ProductionFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProductionAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = SemifinishedDataTypeDefinitionSerialize_List(required=False)      # 父类别信息
    semifinishedDataType_child = SemifinishedDataTypeDefinitionSerialize_List(many=True)  # 子类别信息
    semifinishedDataType_item = SemifinishedDataDefinitionSerialize_Type(many=True)  # 附属项信息

    class Meta:
        model = SemifinishedDataTypeDefinitionModel
        fields = "__all__"


class SemifinishedDataTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    半成品过程数据类型定义--update
    """
    class Meta:
        model = SemifinishedDataTypeDefinitionModel
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
        if not auditor.has_perm('production.admin_semifinishedDatatypedefinitionmodel'):
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
                list = SemifinishedDataTypeDefinitionModel.objects.get(id=value.id)
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


class SemifinishedDataTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    半成品过程数据类型定义--partial
    """
    class Meta:
        model = SemifinishedDataTypeDefinitionModel
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
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = SemifinishedDataTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 半成品过程数据类型层级结构 序列化器
class SemifinishedDataTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    半成品过程数据类型层级结构--fourth
    """
    class Meta:
        model = SemifinishedDataTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class SemifinishedDataTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    半成品过程数据类型层级结构--third
    """
    semifinishedDataType_child = SemifinishedDataTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = SemifinishedDataTypeDefinitionModel
        fields = ("id", "name", "code", "state", "semifinishedDataType_child")

class SemifinishedDataTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    半成品过程数据类型层级结构--second
    """
    semifinishedDataType_child = SemifinishedDataTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = SemifinishedDataTypeDefinitionModel
        fields = ("id", "name", "code", "state", "semifinishedDataType_child")

class SemifinishedDataTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    半成品过程数据类型层级结构--fitst
    """
    semifinishedDataType_child = SemifinishedDataTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = SemifinishedDataTypeDefinitionModel
        fields = ("id", "name", "code", "state","semifinishedDataType_child")

# endregion



# region  生产看板定义  序列化器
class ProductionBoardSerialize_Create(serializers.ModelSerializer):

    """
    生产看板定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductionBoardModel
        fields = ("id", "name", "code","state", "image", "file","desc", "auditor","create_user"
                  )
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_productionboardmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_productionboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class  ProductionBoardSerialize_List(serializers.ModelSerializer):

    """
    生产看板定义--list
    """
    image = ProductionImageSerialize_List()
    class Meta:
        model = ProductionBoardModel
        fields = ("id", "name", "code", "state","image","create_user","auditor","create_time","update_time")


class ProductionBoardSerialize_Retrieve(serializers.ModelSerializer):

    """
    生产看板定义--retrieve
    """
    image = ProductionImageSerialize_List()
    file =ProductionFileSerialize_List(many=True)
    alter = ProductionAlterRecordSerialize_List(many=True)

    class Meta:
        model = ProductionBoardModel
        fields = "__all__"


class ProductionBoardSerialize_Update(serializers.ModelSerializer):
    """
    生产看板定义--update
    """

    class Meta:
        model = ProductionBoardModel
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
        if not auditor.has_perm('production.admin_productionboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class ProductionBoardSerialize_Partial(serializers.ModelSerializer):
    """
    生产看板定义--partial
    """

    class Meta:
        model = ProductionBoardModel
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
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = ProductionBoardModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion