from rest_framework import serializers
from commonFunction import *
from apps.process.models.basicinfor_model import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()

# region  当前APP操作记录 序列化器
class ProcessAuditRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP操作记录---list
    """
    class Meta:
        model = ProcessAuditRecordModel
        fields = ("id", "uri", "uri_id", "time","classes", "user","result")

class ProcessAuditRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    当前APP操作记录---retrieve
    """
    class Meta:
        model = ProcessAuditRecordModel
        fields = "__all__"

# endregion

# region  当前APP审核记录 序列化器
class ProcessAlterRecordSerialize_Create(serializers.ModelSerializer):
    """
    当前APP审核记录--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProcessAlterRecordModel
        fields = ("id", "uri", "desc","create_user", )

class ProcessAlterRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP审核记录---list
    """
    class Meta:
        model = ProcessAlterRecordModel
        fields = "__all__"

# endregion

# region  当前APP文件/图片  序列化器
class ProcessImageSerialize_Create(serializers.ModelSerializer):
    """
    当前APP图片--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProcessImageModel
        fields = ("id", "image", "uri", "desc","create_user")

    def validate(self, attrs):
        attrs["image_name"]=attrs["image"]
        return attrs

class ProcessImageSerialize_List(serializers.ModelSerializer):
    """
    当前APP图片--list
    """
    class Meta:
        model = ProcessImageModel
        fields =  "__all__"

class ProcessFileSerialize_Create(serializers.ModelSerializer):
    """
    当前APP文件--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProcessFileModel
        fields = ("id", "file", "uri", "desc", "create_user")

    def validate(self, attrs):
        attrs["file_name"] = attrs["file"]
        return attrs

class ProcessFileSerialize_List(serializers.ModelSerializer):
    """
    当前APP文件--list
    """
    class Meta:
        model = ProcessFileModel
        fields =  "__all__"

# endregion

# region 计量单位类型定义 序列化器
class UnitTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    计量单位类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UnitTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_unittypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_unittypedefinitionmodel'):
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
                list = UnitTypeDefinitionModel.objects.get(id=value.id)
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


class UnitTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    计量单位类型定义--list
    """
    class Meta:
        model = UnitTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class UnitInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    计量单位定义--计量单位类型定义
    """

    class Meta:
        model = UnitInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class UnitTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    计量单位类型定义--retrieve
    """
    file = ProcessFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProcessAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = UnitTypeDefinitionSerialize_List(required=False)   # 父类别信息
    unitType_child = UnitTypeDefinitionSerialize_List(many=True)# 子类别信息
    unitType_item = UnitInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = UnitTypeDefinitionModel
        fields = "__all__"


class UnitTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    计量单位类型定义--update
    """
    class Meta:
        model = UnitTypeDefinitionModel
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
        if not auditor.has_perm('process.admin_unittypedefinitionmodel'):
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
                list = UnitTypeDefinitionModel.objects.get(id=value.id)
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


class UnitTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    计量单位类型定义--partial
    """
    class Meta:
        model = UnitTypeDefinitionModel
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
        obj = UnitTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 计量单位类型层级结构 序列化器
class UnitTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    计量单位类型层级结构--fourth
    """
    class Meta:
        model = UnitTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class UnitTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    计量单位类型定义--third
    """
    unitType_child = UnitTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = UnitTypeDefinitionModel
        fields = ("id", "name", "code", "state", "unitType_child")

class UnitTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    计量单位类型定义--second
    """
    unitType_child = UnitTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = UnitTypeDefinitionModel
        fields = ("id", "name", "code", "state", "unitType_child")

class UnitTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    计量单位类型定义--fitst
    """
    unitType_child = UnitTypeDefinitionSerialize_Second(many=True) # 子类别信息

    class Meta:
        model = UnitTypeDefinitionModel
        fields = ("id", "name", "code", "state","unitType_child")

# endregion

# region 计量单位定义 序列化器
class UnitInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    计量单位定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UnitInforDefinitionModel
        fields = ("id", "name", "code","state", "type", "symbol","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "file", "desc", "auditor","create_user")

     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_unitinfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_unitinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = UnitTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class UnitInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    计量单位定义--list
    """
    type = UnitTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = UnitInforDefinitionModel
        fields = ("id", "name", "code", "state","type", "symbol","auditor","create_user","create_time","update_time")

class UnitInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    计量单位定义--retrieve
    """
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    type = UnitTypeDefinitionSerialize_List(required=False)

    class Meta:
        model = UnitInforDefinitionModel
        fields = "__all__"

class UnitInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    计量单位定义--update
    """
    class Meta:
        model = UnitInforDefinitionModel
        fields = ("id", "name", "code", "type", "symbol", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "file", "desc", "auditor")

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return  attrs
    
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
        if not auditor.has_perm('process.admin_unitinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = UnitTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class UnitInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    计量单位定义--partial
    """
    class Meta:
        model = UnitInforDefinitionModel
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
        obj = UnitInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 物料类型定义 序列化器
class MaterialTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    物料类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MaterialTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_materialtypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_materialtypedefinitionmodel'):
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
                list = MaterialTypeDefinitionModel.objects.get(id=value.id)
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


class MaterialTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    物料类型定义--list
    """
    class Meta:
        model = MaterialTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class MaterialInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    物料定义--物料类型定义
    """

    class Meta:
        model = MaterialInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class MaterialTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    物料类型定义--retrieve
    """
    file = ProcessFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProcessAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = MaterialTypeDefinitionSerialize_List(required=False)   # 父类别信息
    materialType_child = MaterialTypeDefinitionSerialize_List(many=True)# 子类别信息
    materialType_item = MaterialInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = MaterialTypeDefinitionModel
        fields = "__all__"


class MaterialTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    物料类型定义--update
    """
    class Meta:
        model = MaterialTypeDefinitionModel
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
        if not auditor.has_perm('process.admin_materialtypedefinitionmodel'):
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
                list = MaterialTypeDefinitionModel.objects.get(id=value.id)
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


class MaterialTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    物料类型定义--partial
    """
    class Meta:
        model = MaterialTypeDefinitionModel
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
        obj = MaterialTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 物料类型层级结构 序列化器
class MaterialTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    物料类型层级结构--fourth
    """
    class Meta:
        model = MaterialTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class MaterialTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    物料类型定义--third
    """
    materialType_child = MaterialTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = MaterialTypeDefinitionModel
        fields = ("id", "name", "code", "state", "materialType_child")

class MaterialTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    物料类型定义--second
    """
    materialType_child = MaterialTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = MaterialTypeDefinitionModel
        fields = ("id", "name", "code", "state", "materialType_child")

class MaterialTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    物料类型定义--fitst
    """
    materialType_child = MaterialTypeDefinitionSerialize_Second(many=True) # 子类别信息

    class Meta:
        model = MaterialTypeDefinitionModel
        fields = ("id", "name", "code", "state","materialType_child")

# endregion

# region 物料定义 序列化器
class MaterialInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    物料定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MaterialInforDefinitionModel
        fields = ("id", "name", "code","state", "type", "unit", "purchase_code1",
                  "vendor1", "purchase_code2", "vendor2", "purchase_code3","vendor3","character", "attribute1",
                  "attribute2", "attribute3", "attribute4","attribute5", "attribute6","attribute7", "attribute8","attribute9", "attribute10",
                   "image", "file", "desc", "auditor","create_user")
     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_materialinfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_materialinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = MaterialTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 计量单位字段验证
    def validate_unit(self, value):
        list = UnitInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的计量单位不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的计量单位不在--'使用状态'")
        return value


class MaterialInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    物料定义--list
    """
    type = MaterialTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = MaterialInforDefinitionModel
        fields = ("id", "name", "code", "state","type","character","auditor","create_user","create_time","update_time" )

class MaterialInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    物料定义--retrieve
    """
    image = ProcessImageSerialize_List(many=True)
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    type = MaterialTypeDefinitionSerialize_List(required=False)
    unit = UnitInforDefinitionSerialize_List(required=False)

    class Meta:
        model = MaterialInforDefinitionModel
        fields = "__all__"

class MaterialInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    物料定义--update
    """
    class Meta:
        model = MaterialInforDefinitionModel
        fields = ("id", "name", "code", "type", "unit", "purchase_code1",
                  "vendor1", "purchase_code2", "vendor2", "purchase_code3","vendor3","character", "attribute1",
                  "attribute2", "attribute3", "attribute4","attribute5", "attribute6","attribute7", "attribute8","attribute9", "attribute10",
                   "image", "file", "desc", "auditor",)
     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return  attrs
    
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
        if not auditor.has_perm('process.admin_materialinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = MaterialTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 计量单位字段验证
    def validate_unit(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = UnitInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的计量单位不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的计量单位不在--'使用状态'")
        return value

class MaterialInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    物料定义--partial
    """
    class Meta:
        model = MaterialInforDefinitionModel
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
        obj = MaterialInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion

# region 半成品类型定义 序列化器
class SemifinishedTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    半成品类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_semifinishedtypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_semifinishedtypedefinitionmodel'):
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
                list = SemifinishedTypeDefinitionModel.objects.get(id=value.id)
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


class SemifinishedTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    半成品类型定义--list
    """
    class Meta:
        model = SemifinishedTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class SemifinishedInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    半成品定义--半成品类型定义
    """
    class Meta:
        model = SemifinishedInforDefinitionModel
        fields = ("id", "name", "code", "state","auditor", "create_user")




class SemifinishedTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品类型定义--retrieve
    """
    file = ProcessFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProcessAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = SemifinishedTypeDefinitionSerialize_List(required=False)   # 父类别信息
    semifinishedType_child = SemifinishedTypeDefinitionSerialize_List(many=True)# 子类别信息
    semifinishedType_item = SemifinishedInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = SemifinishedTypeDefinitionModel
        fields = "__all__"


class SemifinishedTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    半成品类型定义--update
    """
    class Meta:
        model = SemifinishedTypeDefinitionModel
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
        if not auditor.has_perm('process.admin_semifinishedtypedefinitionmodel'):
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
                list = SemifinishedTypeDefinitionModel.objects.get(id=value.id)
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


class SemifinishedTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    半成品类型定义--partial
    """
    class Meta:
        model = SemifinishedTypeDefinitionModel
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
        obj = SemifinishedTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 半成品类型层级结构 序列化器
class SemifinishedTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    半成品类型层级结构--fourth
    """
    class Meta:
        model = SemifinishedTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class SemifinishedTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    半成品类型定义--third
    """
    semifinishedType_child = SemifinishedTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = SemifinishedTypeDefinitionModel
        fields = ("id", "name", "code", "state", "semifinishedType_child")

class SemifinishedTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    半成品类型定义--second
    """
    semifinishedType_child = SemifinishedTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = SemifinishedTypeDefinitionModel
        fields = ("id", "name", "code", "state", "semifinishedType_child")

class SemifinishedTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    半成品类型定义--fitst
    """
    semifinishedType_child = SemifinishedTypeDefinitionSerialize_Second(many=True) # 子类别信息

    class Meta:
        model = SemifinishedTypeDefinitionModel
        fields = ("id", "name", "code", "state","semifinishedType_child")

# endregion

# region 半成品定义 序列化器
class SemifinishedInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    半成品定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedInforDefinitionModel
        fields = ("id", "name", "code", "state", "type", "unit", "route_id",
                  "attribute1", "attribute2", "attribute3", "attribute4", "attribute5", "attribute6",
                  "attribute7", "attribute8", "attribute9", "attribute10", "image", "file",
                  "desc", "auditor", "create_user"
                  )

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_semifinishedinfordefinitionmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        if 'route_id' in attrs.keys():
            if attrs['route_id'] is not '':
                try:
                    route = ProductRouteDefinitionModel.objects.get(id=attrs["route_id"])  # 判断指定的产品是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的生产线路不存在")
                attrs["routeType_code"] = route.type.code  # 获取生产线路类型编码
                attrs["routeType_name"] = route.type.name  # 获取生产线路类型名称
                attrs["route_code"] = route.code  # 获取生产线路编码
                attrs["route_name"] = route.name  # 获取生产线路名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('process.admin_semifinishedinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = SemifinishedTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 计量单位字段验证
    def validate_unit(self, value):
        list = UnitInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的计量单位不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的计量单位不在--'使用状态'")
        return value

    # 生产线路字段验证
    def validate_product_route(self, value):
        if len(value) ==0 :
            return value
        list = ProductRouteDefinitionModel.objects.get(id=int(value))
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的生产线路不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的生产线路不在--'使用状态'")
        return value


class SemifinishedInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    半成品定义--list
    """
    type = SemifinishedTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = SemifinishedInforDefinitionModel
        fields = ("id", "name", "code", "state","type","auditor", "create_user","create_time","update_time")


class ProductRouteDefinitionSerialize_Semifinished(serializers.ModelSerializer):
    """
    生产路线定义--半成品定义
    """

    class Meta:
        model = ProductRouteDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")


class SemifinishedInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品定义--retrieve
    """
    image = ProcessImageSerialize_List(many=True)
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    type = SemifinishedTypeDefinitionSerialize_List(required=False)
    unit = UnitInforDefinitionSerialize_List(required=False)

    class Meta:
        model = SemifinishedInforDefinitionModel
        fields = "__all__"

class SemifinishedInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    半成品定义--update
    """
    class Meta:
        model = SemifinishedInforDefinitionModel
        fields = ("id", "name", "code", "type", "unit", "route_id",
                  "attribute1", "attribute2", "attribute3", "attribute4", "attribute5",
                  "attribute6", "attribute7", "attribute8", "attribute9", "attribute10",
                  "image", "file","desc", "auditor"
                  )

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if 'route_id' in attrs.keys():
            if attrs['route_id'] is not '':
                try:
                    route = ProductRouteDefinitionModel.objects.get(id=attrs["route_id"])  # 判断指定的产品是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的生产线路不存在")
                attrs["routeType_code"] = route.type.code  # 获取生产线路类型编码
                attrs["routeType_name"] = route.type.name  # 获取生产线路类型名称
                attrs["route_code"] = route.code  # 获取生产线路编码
                attrs["route_name"] = route.name  # 获取生产线路名称
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
        if not auditor.has_perm('process.admin_semifinishedinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = SemifinishedTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 计量单位字段验证
    def validate_unit(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = UnitInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的计量单位不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的计量单位不在--'使用状态'")
        return value

    # 生产线路字段验证
    def validate_route_id(self, value):
        if len(value) ==0 :
            return value
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = ProductRouteDefinitionModel.objects.get(id=int(value))
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的生产线路不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的生产线路不在--'使用状态'")
        return value


class SemifinishedInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    半成品定义--partial
    """

    class Meta:
        model = SemifinishedInforDefinitionModel
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
        obj = SemifinishedInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 产品类型定义 序列化器
class ProductTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    产品类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_producttypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_producttypedefinitionmodel'):
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
                list = ProductTypeDefinitionModel.objects.get(id=value.id)
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


class ProductTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    产品类型定义--list
    """
    class Meta:
        model = ProductTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class ProductInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    产品定义--产品类型定义
    """

    class Meta:
        model = ProductInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class ProductTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品类型定义--retrieve
    """
    file = ProcessFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProcessAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = ProductTypeDefinitionSerialize_List(required=False)   # 父类别信息
    productType_child = ProductTypeDefinitionSerialize_List(many=True)# 子类别信息
    productType_item = ProductInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = ProductTypeDefinitionModel
        fields = "__all__"


class ProductTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    产品类型定义--update
    """
    class Meta:
        model = ProductTypeDefinitionModel
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
        if not auditor.has_perm('process.admin_producttypedefinitionmodel'):
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
                list = ProductTypeDefinitionModel.objects.get(id=value.id)
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


class ProductTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    产品类型定义--partial
    """
    class Meta:
        model = ProductTypeDefinitionModel
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
        obj = ProductTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 产品类型层级结构 序列化器
class ProductTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    产品类型层级结构--fourth
    """
    class Meta:
        model = ProductTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class ProductTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    产品类型定义--third
    """
    productType_child = ProductTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = ProductTypeDefinitionModel
        fields = ("id", "name", "code", "state", "productType_child")

class ProductTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    产品类型定义--second
    """
    productType_child = ProductTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = ProductTypeDefinitionModel
        fields = ("id", "name", "code", "state", "productType_child")

class ProductTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    产品类型定义--fitst
    """
    productType_child = ProductTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = ProductTypeDefinitionModel
        fields = ("id", "name", "code", "state","productType_child")

# endregion

# region 产品定义 序列化器
class ProductInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    产品定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductInforDefinitionModel
        fields = ("id", "name", "code","state",  "type", "unit", "route_id",
                   "attribute1", "attribute2","attribute3", "attribute4","attribute5", "attribute6",
                  "attribute7",  "attribute8","attribute9", "attribute10",  "image", "file",
                  "desc", "auditor","create_user"
                  )

     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_productinfordefinitionmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        if 'route_id' in attrs.keys():
            if attrs['route_id'] is not '':
                try:
                    route = ProductRouteDefinitionModel.objects.get(id=attrs["route_id"])  # 判断指定的产品是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的生产线路不存在")
                attrs["routeType_code"] = route.type.code  # 获取生产线路类型编码
                attrs["routeType_name"] = route.type.name  # 获取生产线路类型名称
                attrs["route_code"] = route.code  # 获取生产线路编码
                attrs["route_name"] = route.name  # 获取生产线路名称
        return attrs
    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('process.admin_productinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = ProductTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 计量单位字段验证
    def validate_unit(self, value):
        list = UnitInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的计量单位不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的计量单位不在--'使用状态'")
        return value

    # 生产线路字段验证
    def validate_route_id(self, value):
        if len(value) ==0 :
            return value
        list = ProductRouteDefinitionModel.objects.get(id=int(value))
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的生产线路不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的生产线路不在--'使用状态'")
        return value


class ProductInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    产品定义--list
    """
    type = ProductTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = ProductInforDefinitionModel
        fields = ("id", "name", "code", "state", "type","auditor","create_user","create_time","update_time")

class ProductRouteDefinitionSerialize_Product(serializers.ModelSerializer):
    """
    生产路线定义--产品定义
    """
    class Meta:
        model = ProductRouteDefinitionModel
        fields = ("id", "name", "code", "state", "auditor","create_user")

class ProductInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品定义--retrieve
    """
    image = ProcessImageSerialize_List(many=True)
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    type = ProductTypeDefinitionSerialize_List(required=False)
    unit = UnitInforDefinitionSerialize_List(required=False)

    class Meta:
        model = ProductInforDefinitionModel
        fields = "__all__"

class ProductInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    产品定义--update
    """
    class Meta:
        model = ProductInforDefinitionModel
        fields = ("id", "name", "code", "type", "unit", "route_id",
                   "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "attribute6","attribute7", "attribute8","attribute9", "attribute10", "image", "file",
                  "desc", "auditor"
                  )
        
     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if 'route_id' in attrs.keys():
            if attrs['route_id'] is not '':
                try:
                    route = ProductRouteDefinitionModel.objects.get(id=attrs["route_id"])  # 判断指定的产品是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的生产线路不存在")
                attrs["routeType_code"] = route.type.code  # 获取生产线路类型编码
                attrs["routeType_name"] = route.type.name  # 获取生产线路类型名称
                attrs["route_code"] = route.code  # 获取生产线路编码
                attrs["route_name"] = route.name  # 获取生产线路名称
        return  attrs
    
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
        if not auditor.has_perm('process.admin_productinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = ProductTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 计量单位字段验证
    def validate_unit(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = UnitInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的计量单位不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的计量单位不在--'使用状态'")
        return value

    # 生产线路字段验证
    def validate_route_id(self, value):
        if len(value) ==0 :
            return value
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = ProductRouteDefinitionModel.objects.get(id=int(value))
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的生产线路不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的生产线路不在--'使用状态'")
        return value

class ProductInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    产品定义--partial
    """
    class Meta:
        model = ProductInforDefinitionModel
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
        obj = ProductInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 工位类型定义 序列化器
class StationTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    工位类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = StationTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_stationtypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_stationtypedefinitionmodel'):
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
                list = StationTypeDefinitionModel.objects.get(id=value.id)
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


class StationTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    工位类型定义--list
    """
    class Meta:
        model = StationTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class StationInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    工位定义--工位类型定义
    """

    class Meta:
        model = StationInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class StationTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    工位类型定义--retrieve
    """
    file = ProcessFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProcessAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = StationTypeDefinitionSerialize_List(required=False)   # 父类别信息
    stationType_child = StationTypeDefinitionSerialize_List(many=True)# 子类别信息
    stationType_item = StationInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = StationTypeDefinitionModel
        fields = "__all__"


class StationTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    工位类型定义--update
    """
    class Meta:
        model = StationTypeDefinitionModel
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
        if not auditor.has_perm('process.admin_stationtypedefinitionmodel'):
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
                list = StationTypeDefinitionModel.objects.get(id=value.id)
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


class StationTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    工位类型定义--partial
    """
    class Meta:
        model = StationTypeDefinitionModel
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
        obj = StationTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 工位类型层级结构 序列化器
class StationTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    工位类型层级结构--fourth
    """
    class Meta:
        model = StationTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class StationTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    工位类型定义--third
    """
    stationType_child = StationTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = StationTypeDefinitionModel
        fields = ("id", "name", "code", "state", "stationType_child")

class StationTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    工位类型定义--second
    """
    stationType_child = StationTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = StationTypeDefinitionModel
        fields = ("id", "name", "code", "state", "stationType_child")

class StationTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    工位类型定义--fitst
    """
    stationType_child = StationTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = StationTypeDefinitionModel
        fields = ("id", "name", "code", "state","stationType_child")

# endregion

# region 工位物料定义 序列化器
class StationMaterialSerialize_Create(serializers.ModelSerializer):
    """
    工位物料--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = StationMaterialModel
        fields = ("id", "material", "sum", "desc","create_user")


class StationMaterialSerialize_List(serializers.ModelSerializer):
    """
    工位物料--list
    """
    material = MaterialInforDefinitionSerialize_List()
    class Meta:
        model = StationMaterialModel
        fields =  "__all__"

# endregion

# region 工位半成品定义 序列化器
class StationSemifinishedSerialize_Create(serializers.ModelSerializer):
    """
    工位半成品--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = StationSemifinishedModel
        fields = ("id", "semifinished", "sum", "desc","create_user")

class StationSemifinishedSerialize_List(serializers.ModelSerializer):
    """
    工位半成品--list
    """
    semifinished = SemifinishedInforDefinitionSerialize_List()

    class Meta:
        model = StationSemifinishedModel
        fields =  "__all__"

# endregion

# region 工位定义 序列化器
class StationInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    工位定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = StationInforDefinitionModel
        fields = ("id", "name", "code", "state","type","material","semifinished", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "image", "file", "desc", "auditor","create_user")

     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_stationinfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_stationinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = StationTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class StationInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    工位定义--list
    """
    type = StationTypeDefinitionSerialize_List()
    class Meta:
        model = StationInforDefinitionModel
        fields = ("id", "name", "code", "state","type","auditor","create_user","create_time","update_time")

class StationInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    工位定义--retrieve
    """
    image = ProcessImageSerialize_List(many=True)
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    material = StationMaterialSerialize_List(many=True)
    semifinished=StationSemifinishedSerialize_List(many=True)
    type = StationTypeDefinitionSerialize_List()

    class Meta:
        model = StationInforDefinitionModel
        fields = "__all__"

class StationInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    工位定义--update
    """
    class Meta:
        model = StationInforDefinitionModel
        fields = ("id", "name", "code","type","material","semifinished", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "image", "file", "desc", "auditor")

     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return  attrs
    
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
        if not auditor.has_perm('process.admin_stationinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = StationTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class StationInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    工位定义--partial
    """
    class Meta:
        model = StationInforDefinitionModel
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
        obj = StationInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 生产线路类型定义 序列化器
class ProductRouteTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    生产线路类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductRouteTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_productroutetypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_productroutetypedefinitionmodel'):
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
                list = ProductRouteTypeDefinitionModel.objects.get(id=value.id)
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


class ProductRouteTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    生产线路类型定义--list
    """
    class Meta:
        model = ProductRouteTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class ProductRouteInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    生产线路定义--生产线路类型定义
    """

    class Meta:
        model = ProductRouteDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class ProductRouteTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    生产线路类型定义--retrieve
    """
    file = ProcessFileSerialize_List(many=True)                 # 类型文件信息
    alter = ProcessAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = ProductRouteTypeDefinitionSerialize_List(required=False)   # 父类别信息
    productRouteType_child = ProductRouteTypeDefinitionSerialize_List(many=True)# 子类别信息
    productRouteType_item = ProductRouteInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = ProductRouteTypeDefinitionModel
        fields = "__all__"


class ProductRouteTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    生产线路类型定义--update
    """
    class Meta:
        model = ProductRouteTypeDefinitionModel
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
        if not auditor.has_perm('process.admin_productroutetypedefinitionmodel'):
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
                list = ProductRouteTypeDefinitionModel.objects.get(id=value.id)
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


class ProductRouteTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    生产线路类型定义--partial
    """
    class Meta:
        model = ProductRouteTypeDefinitionModel
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
        obj = ProductRouteTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 生产线路类型层级结构 序列化器
class ProductRouteTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    生产线路类型层级结构--fourth
    """
    class Meta:
        model = ProductRouteTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class ProductRouteTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    生产线路类型定义--third
    """
    productRouteType_child = ProductRouteTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = ProductRouteTypeDefinitionModel
        fields = ("id", "name", "code", "state", "productRouteType_child")

class ProductRouteTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    生产线路类型定义--second
    """
    productRouteType_child = ProductRouteTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = ProductRouteTypeDefinitionModel
        fields = ("id", "name", "code", "state", "productRouteType_child")

class ProductRouteTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    生产线路类型定义--fitst
    """
    productRouteType_child = ProductRouteTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = ProductRouteTypeDefinitionModel
        fields = ("id", "name", "code", "state","productRouteType_child")

# endregion

# region 生产路线定义 序列化器
class ProductRouteDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    生产路线定义--create
    """

    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductRouteDefinitionModel
        fields = ("id", "name", "code", "state","type", "station","attribute1","attribute2",
                  "attribute3", "attribute4","attribute5", "file", "desc", "auditor","create_user")

     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_productroutedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('process.admin_productroutedefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = ProductRouteTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class ProductRouteDefinitionSerialize_List(serializers.ModelSerializer):
    """
    生产路线定义--list
    """
    type = ProductRouteTypeDefinitionSerialize_List()
    class Meta:
        model = ProductRouteDefinitionModel
        fields = ("id", "name", "code", "state","type", "auditor","create_user","create_time","update_time")

class ProductRouteDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    生产路线定义--retrieve
    """
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    type = ProductRouteTypeDefinitionSerialize_List()
    station= StationInforDefinitionSerialize_List(many=True)
    class Meta:
        model = ProductRouteDefinitionModel
        fields = "__all__"

class ProductRouteDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    生产路线定义--update
    """
    class Meta:
        model = ProductRouteDefinitionModel
        fields = ("id", "name", "code", "type","station", "attribute1","attribute2",
                  "attribute3", "attribute4","attribute5", "file", "desc", "auditor")

     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return  attrs
    
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
        if not auditor.has_perm('process.admin_productroutedefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = ProductRouteTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class ProductRouteDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    生产路线定义--partial
    """
    class Meta:
        model = ProductRouteDefinitionModel
        fields = ("id", "state","alter")

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
        obj = ProductRouteDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion

# region  工艺信息浏览  序列化器

class MaterialInforDefinitionSerialize(serializers.ModelSerializer):
    """
    物料信息
    """
    image = ProcessImageSerialize_List(many=True)
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    type = MaterialTypeDefinitionSerialize_List(required=False)
    unit = UnitInforDefinitionSerialize_List(required=False)

    class Meta:
        model = MaterialInforDefinitionModel
        fields = "__all__"


class SemifinishedInforDefinitionSerialize(serializers.ModelSerializer):
    """
    半成品信息
    """
    image = ProcessImageSerialize_List(many=True)
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    type = SemifinishedTypeDefinitionSerialize_List(required=False)
    unit = UnitInforDefinitionSerialize_List(required=False)


    class Meta:
        model = SemifinishedInforDefinitionModel
        fields = "__all__"

class StationMaterialSerialize(serializers.ModelSerializer):
    """
    工位物料
    """
    material = MaterialInforDefinitionSerialize()
    class Meta:
        model = StationMaterialModel
        fields =  "__all__"


class StationSemifinishedSerialize(serializers.ModelSerializer):
    """
    工位半成品
    """
    semifinished = SemifinishedInforDefinitionSerialize()

    class Meta:
        model = StationSemifinishedModel
        fields =  "__all__"

class StationInforDefinitionSerialize(serializers.ModelSerializer):
    """
    工位信息
    """
    image = ProcessImageSerialize_List(many=True)
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    material = StationMaterialSerialize(many=True)
    semifinished=StationSemifinishedSerialize(many=True)
    type = StationTypeDefinitionSerialize_List()

    class Meta:
        model = StationInforDefinitionModel
        fields = "__all__"

class ProcessInforSerialize(serializers.ModelSerializer):
    """
    生产路线信息(工艺信息)
    """
    file = ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    type = ProductRouteTypeDefinitionSerialize_List()
    station= StationInforDefinitionSerialize(many=True)
    class Meta:
        model = ProductRouteDefinitionModel
        fields = "__all__"

# endregion
# region  工艺看板定义  序列化器
class ProcessBoardSerialize_Create(serializers.ModelSerializer):

    """
    工艺看板定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProcessBoardModel
        fields = ("id", "name", "code","state", "image", "file","desc", "auditor","create_user"
                  )
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('process.add_processboardmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True:
            if attrs["create_user"].username == attrs["auditor"]:  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        return  attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('process.admin_processboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class  ProcessBoardSerialize_List(serializers.ModelSerializer):

    """
    工艺看板定义--list
    """
    image = ProcessImageSerialize_List()
    class Meta:
        model = ProcessBoardModel
        fields = ("id", "name", "code", "state","image","create_user","auditor","create_time","update_time")


class ProcessBoardSerialize_Retrieve(serializers.ModelSerializer):

    """
    工艺看板定义--retrieve
    """
    image = ProcessImageSerialize_List()
    file =ProcessFileSerialize_List(many=True)
    alter = ProcessAlterRecordSerialize_List(many=True)
    class Meta:
        model = ProcessBoardModel
        fields = "__all__"


class ProcessBoardSerialize_Update(serializers.ModelSerializer):
    """
    工艺看板定义--update
    """

    class Meta:
        model = ProcessBoardModel
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
        if not auditor.has_perm('process.admin_processboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class ProcessBoardSerialize_Partial(serializers.ModelSerializer):
    """
    工艺看板定义--partial
    """

    class Meta:
        model = ProcessBoardModel
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
        obj = ProcessBoardModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion
