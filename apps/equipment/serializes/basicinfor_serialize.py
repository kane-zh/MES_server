from rest_framework import serializers
from apps.equipment.models.basicinfor_model import *
from apps.equipment.models.recording_model import *
from commonFunction import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()

# region  当前APP操作记录 序列化器
class EquipmentAuditRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP操作记录---list
    """
    class Meta:
        model = EquipmentAuditRecordModel
        fields = ("id", "uri", "uri_id", "time","classes", "user","result")

class EquipmentAuditRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    当前APP操作记录---retrieve
    """
    class Meta:
        model = EquipmentAuditRecordModel
        fields = "__all__"

# endregion

# region  当前APP审核记录 序列化器
class EquipmentAlterRecordSerialize_Create(serializers.ModelSerializer):
    """
    当前APP审核记录--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentAlterRecordModel
        fields = ("id", "uri", "desc","create_user", )

class EquipmentAlterRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP审核记录---list
    """
    class Meta:
        model = EquipmentAlterRecordModel
        fields = "__all__"

# endregion

# region  当前APP文件/图片  序列化器
class EquipmentImageSerialize_Create(serializers.ModelSerializer):
    """
    当前APP图片--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentImageModel
        fields = ("id", "image", "uri", "desc","create_user")

    def validate(self, attrs):
        attrs["image_name"]=attrs["image"]
        return attrs

class EquipmentImageSerialize_List(serializers.ModelSerializer):
    """
    当前APP图片--list
    """
    class Meta:
        model = EquipmentImageModel
        fields =  "__all__"

class EquipmentFileSerialize_Create(serializers.ModelSerializer):
    """
    当前APP文件--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentFileModel
        fields = ("id", "file", "uri", "desc", "create_user")

    def validate(self, attrs):
        attrs["file_name"] = attrs["file"]
        return attrs

class EquipmentFileSerialize_List(serializers.ModelSerializer):
    """
    当前APP文件--list
    """
    class Meta:
        model = EquipmentFileModel
        fields =  "__all__"

# endregion

# region  设备厂商信息定义  序列化器
class EquipmentVendorDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    设备厂商信息定义 --create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentVendorDefinitionModel
        fields = ("id", "name", "code", "state",  "image", "file", "address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor",
                  "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_equipmentvendordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('equipment.admin_equipmentvendordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class EquipmentVendorDefinitionSerialize_List(serializers.ModelSerializer):
    """
    设备厂商信息定义--list
    """

    class Meta:
        model = EquipmentVendorDefinitionModel
        fields = ("id", "name", "code", "state", "address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre","auditor","create_user","create_time","update_time")


class EquipmentVendorDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    设备厂商信息定义--retrieve
    """
    image = EquipmentImageSerialize_List(many=True)
    file = EquipmentFileSerialize_List(many=True)
    alter = EquipmentAlterRecordSerialize_List(many=True)

    class Meta:
        model = EquipmentVendorDefinitionModel
        fields = "__all__"


class EquipmentVendorDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    设备厂商信息定义--update
    """

    class Meta:
        model = EquipmentVendorDefinitionModel
        fields = ("id", "name", "code", "image", "file", "address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor",
                  )

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
        if not auditor.has_perm('equipment.admin_equipmentvendordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class EquipmentVendorDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    设备厂商信息定义--partial
    """

    class Meta:
        model = EquipmentVendorDefinitionModel
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
        obj = EquipmentVendorDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 配件类型定义 序列化器
class PartsTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    配件类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PartsTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_partstypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('equipment.admin_partstypedefinitionmodel'):
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
                list = PartsTypeDefinitionModel.objects.get(id=value.id)
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


class PartsTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    配件类型定义--list
    """
    class Meta:
        model = PartsTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class PartsInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    配件定义--配件类型定义
    """

    class Meta:
        model = PartsInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class PartsTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    配件类型定义--retrieve
    """
    file = EquipmentFileSerialize_List(many=True)                 # 类型文件信息
    alter = EquipmentAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = PartsTypeDefinitionSerialize_List(required=False)   # 父类别信息
    partsType_child = PartsTypeDefinitionSerialize_List(many=True)# 子类别信息
    partsType_item = PartsInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = PartsTypeDefinitionModel
        fields = "__all__"


class PartsTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    配件类型定义--update
    """
    class Meta:
        model = PartsTypeDefinitionModel
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
        if not auditor.has_perm('equipment.admin_partstypedefinitionmodel'):
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
                list = PartsTypeDefinitionModel.objects.get(id=value.id)
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


class PartsTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    配件类型定义--partial
    """
    class Meta:
        model = PartsTypeDefinitionModel
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
        obj = PartsTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 配件类型层级结构 序列化器
class PartsTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    配件类型层级结构--fourth
    """
    class Meta:
        model = PartsTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class PartsTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    配件类型层级结构--third
    """
    partsType_child = PartsTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = PartsTypeDefinitionModel
        fields = ("id", "name", "code", "state", "partsType_child")

class PartsTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    配件类型层级结构--second
    """
    partsType_child = PartsTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = PartsTypeDefinitionModel
        fields = ("id", "name", "code", "state", "partsType_child")

class PartsTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    配件类型层级结构--fitst
    """
    partsType_child = PartsTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = PartsTypeDefinitionModel
        fields = ("id", "name", "code", "state","partsType_child")

# endregion

# region 配件信息 序列化器
class PartsInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    配件信息--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PartsInforDefinitionModel
        fields = ("id", "name", "code", "state","type", "vendor","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",  "image", "file", "desc", "auditor",
                  "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_partsinfordefinitionmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        if attrs['state'] == "审核中":
            if self.instance.vendor.state != "使用中":  # 如果指定的供应商不是’使用中状态‘
                raise serializers.ValidationError("指定的父类别非‘使用中’状态")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('equipment.admin_partsinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = PartsTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class PartsInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    配件信息--list
    """
    type = PartsTypeDefinitionSerialize_List()
    class Meta:
        model = PartsInforDefinitionModel
        fields = ("id", "name", "code", "state", "type","auditor", "create_user","create_time","update_time"
                  )


class PartsInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    配件信息--retrieve
    """
    image = EquipmentImageSerialize_List(many=True)
    file = EquipmentFileSerialize_List(many=True)
    alter = EquipmentAlterRecordSerialize_List(many=True)
    vendor = EquipmentVendorDefinitionSerialize_List()
    type =  PartsTypeDefinitionSerialize_List()

    class Meta:
        model = PartsInforDefinitionModel
        fields = "__all__"


class PartsInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    配件信息--update
    """
    class Meta:
        model = PartsInforDefinitionModel
        fields = ("id", "name", "code","type", "vendor", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "image", "file", "desc", "auditor",)
        
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
        if not auditor.has_perm('equipment.admin_partsinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = PartsTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class PartsInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    配件信息--partial
    """

    class Meta:
        model = PartsInforDefinitionModel
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
        obj = PartsInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion

# region 设备类型定义 序列化器
class EquipmentTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    设备类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_equipmenttypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('equipment.admin_equipmenttypedefinitionmodel'):
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
                list = EquipmentTypeDefinitionModel.objects.get(id=value.id)
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


class EquipmentTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    设备类型定义--list
    """
    class Meta:
        model = EquipmentTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class EquipmentInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    设备定义--设备类型定义
    """

    class Meta:
        model = EquipmentAccountModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class EquipmentTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    设备类型定义--retrieve
    """
    file = EquipmentFileSerialize_List(many=True)                 # 类型文件信息
    alter = EquipmentAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = EquipmentTypeDefinitionSerialize_List(required=False)   # 父类别信息
    equipmentType_child = EquipmentTypeDefinitionSerialize_List(many=True)# 子类别信息
    equipmentType_item = EquipmentInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = EquipmentTypeDefinitionModel
        fields = "__all__"


class EquipmentTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    设备类型定义--update
    """
    class Meta:
        model = EquipmentTypeDefinitionModel
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
        if not auditor.has_perm('equipment.admin_equipmenttypedefinitionmodel'):
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
                list = EquipmentTypeDefinitionModel.objects.get(id=value.id)
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


class EquipmentTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    设备类型定义--partial
    """
    class Meta:
        model = EquipmentTypeDefinitionModel
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
        obj = EquipmentTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 设备类型层级结构 序列化器
class EquipmentTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    设备类型层级结构--fourth
    """
    class Meta:
        model = EquipmentTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class EquipmentTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    设备类型层级结构--third
    """
    equipmentType_child = EquipmentTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = EquipmentTypeDefinitionModel
        fields = ("id", "name", "code", "state", "equipmentType_child")

class EquipmentTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    设备类型层级结构--second
    """
    equipmentType_child = EquipmentTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = EquipmentTypeDefinitionModel
        fields = ("id", "name", "code", "state", "equipmentType_child")

class EquipmentTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    设备类型层级结构--fitst
    """
    equipmentType_child = EquipmentTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = EquipmentTypeDefinitionModel
        fields = ("id", "name", "code", "state","equipmentType_child")

# endregion

# region 设备台账定义 序列化器
class EquipmentAccountSerialize_Create(serializers.ModelSerializer):
    """
    设备台账定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentAccountModel
        fields = ("id", "name", "code", "state","type","vendor","parts", "affiliation","location","principal","depreciationRate",
                  "dataOfActivation","dataOfPurchase", "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "image", "file","desc", "auditor", "create_user"
                  )

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_equipmentaccountmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('equipment.admin_equipmentaccountmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = EquipmentTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value



class EquipmentAccountSerialize_List(serializers.ModelSerializer):
    """
    设备台账定义--list
    """
    type = EquipmentTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = EquipmentAccountModel
        fields = ("id", "name", "code", "state","type", "auditor", "create_user","create_time","update_time")

class EquipmentAccountSerialize_Retrieve(serializers.ModelSerializer):
    """
    设备台账定义--retrieve
    """
    image =EquipmentImageSerialize_List(many=True)
    file =EquipmentFileSerialize_List(many=True)
    alter =EquipmentAlterRecordSerialize_List(many=True)
    type = EquipmentTypeDefinitionSerialize_List(required=False)
    vendor=EquipmentVendorDefinitionSerialize_List()
    parts = PartsInforDefinitionSerialize_List(many=True)

    class Meta:
        model = EquipmentAccountModel
        fields = "__all__"


class EquipmentAccountSerialize_Update(serializers.ModelSerializer):
    """
    设备台账定义--update
    """

    class Meta:
        model = EquipmentAccountModel
        fields = ("id", "name", "code",  "type","parts", "affiliation","location","principal","depreciationRate","vendor",
                  "dataOfActivation","dataOfPurchase", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "image", "file","desc", "auditor", )

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
        if not auditor.has_perm('equipment.admin_equipmentaccountmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = EquipmentTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class EquipmentAccountSerialize_Partial(serializers.ModelSerializer):
    """
    设备台账定义--partial
    """

    class Meta:
        model = EquipmentAccountModel
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
        obj = EquipmentAccountModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 维护记录类型定义 序列化器
class MaintainRecordTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    维护记录类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MaintainRecordTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_maintainrecordtypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('equipment.admin_maintainrecordtypedefinitionmodel'):
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
                list = MaintainRecordTypeDefinitionModel.objects.get(id=value.id)
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


class MaintainRecordTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    维护记录类型定义--list
    """
    class Meta:
        model = MaintainRecordTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class MaintainRecordInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    维护记录定义--维护记录类型定义
    """

    class Meta:
        model = MaintainRecordModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class MaintainRecordTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    维护记录类型定义--retrieve
    """
    file = EquipmentFileSerialize_List(many=True)                 # 类型文件信息
    alter = EquipmentAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = MaintainRecordTypeDefinitionSerialize_List(required=False)   # 父类别信息
    maintainRecordType_child = MaintainRecordTypeDefinitionSerialize_List(many=True)# 子类别信息
    maintainRecordType_item = MaintainRecordInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = MaintainRecordTypeDefinitionModel
        fields = "__all__"


class MaintainRecordTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    维护记录类型定义--update
    """
    class Meta:
        model = MaintainRecordTypeDefinitionModel
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
        if not auditor.has_perm('equipment.admin_maintainrecordtypedefinitionmodel'):
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
                list = MaintainRecordTypeDefinitionModel.objects.get(id=value.id)
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


class MaintainRecordTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    维护记录类型定义--partial
    """
    class Meta:
        model = MaintainRecordTypeDefinitionModel
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
        obj = MaintainRecordTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 维护记录类型层级结构 序列化器
class MaintainRecordTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    维护记录类型层级结构--fourth
    """
    class Meta:
        model = MaintainRecordTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class MaintainRecordTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    维护记录类型层级结构--third
    """
    maintainRecordType_child = MaintainRecordTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = MaintainRecordTypeDefinitionModel
        fields = ("id", "name", "code", "state", "maintainRecordType_child")

class MaintainRecordTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    维护记录类型层级结构--second
    """
    maintainRecordType_child = MaintainRecordTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = MaintainRecordTypeDefinitionModel
        fields = ("id", "name", "code", "state", "maintainRecordType_child")

class MaintainRecordTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    维护记录类型层级结构--fitst
    """
    maintainRecordType_child = MaintainRecordTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = MaintainRecordTypeDefinitionModel
        fields = ("id", "name", "code", "state","maintainRecordType_child")
# endregion

# region  设备看板定义  序列化器
class EquipmentBoardSerialize_Create(serializers.ModelSerializer):

    """
    设备看板定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentBoardModel
        fields = ("id", "name", "code","state", "image", "file","desc", "auditor","create_user"
                  )
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_equipmentboardmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('equipment.admin_equipmentboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class  EquipmentBoardSerialize_List(serializers.ModelSerializer):

    """
    设备看板定义--list
    """
    image = EquipmentImageSerialize_List()
    class Meta:
        model = EquipmentBoardModel
        fields = ("id", "name", "code", "state","image","create_user","auditor","create_time","update_time")


class EquipmentBoardSerialize_Retrieve(serializers.ModelSerializer):

    """
    设备看板定义--retrieve
    """
    image = EquipmentImageSerialize_List()
    file =EquipmentFileSerialize_List(many=True)
    alter = EquipmentAlterRecordSerialize_List(many=True)
    class Meta:
        model = EquipmentBoardModel
        fields = "__all__"


class EquipmentBoardSerialize_Update(serializers.ModelSerializer):
    """
    设备看板定义--update
    """

    class Meta:
        model = EquipmentBoardModel
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
        if not auditor.has_perm('equipment.admin_equipmentboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class EquipmentBoardSerialize_Partial(serializers.ModelSerializer):
    """
    设备看板定义--partial
    """

    class Meta:
        model = EquipmentBoardModel
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
        obj = EquipmentBoardModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion