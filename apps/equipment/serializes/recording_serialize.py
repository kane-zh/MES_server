from rest_framework import serializers
from apps.equipment.models.recording_model import *
from apps.equipment.serializes.basicinfor_serialize import *
from commonFunction import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()


# region  配件消耗记录定义  序列化器
class PartsUseRecordSerialize_Create(serializers.ModelSerializer):
    """
    配件消耗记录定义 --create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PartsUseRecordModel
        fields = ("id", "name", "code", "state", "file", "parts", "sum",
                  "dataTime", "handler", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor","create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_partsuserecordmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('equipment.admin_partsuserecordmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 配件字段验证
    def validate_parts(self, value):
        list = PartsInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的配件不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的配件不在--'使用状态'")
        return value


class PartsUseRecordSerialize_List(serializers.ModelSerializer):
    """
    配件消耗记录定义--list
    """

    class Meta:
        model = PartsUseRecordModel
        fields = ("id", "name", "code", "state", "sum","dataTime", "handler",
                  "auditor","create_user","create_time","update_time")

class PartsUseRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    配件消耗记录定义--retrieve
    """
    file = EquipmentFileSerialize_List(many=True)
    alter = EquipmentAlterRecordSerialize_List(many=True)
    parts = PartsInforDefinitionSerialize_List()

    class Meta:
        model = PartsUseRecordModel
        fields = "__all__"


class PartsUseRecordSerialize_Update(serializers.ModelSerializer):
    """
    配件消耗记录定义--update
    """

    class Meta:
        model = PartsUseRecordModel
        fields = ("id", "name", "code", "file", "parts", "sum",
                  "dataTime", "handler","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",  "desc", "auditor")

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
        if not auditor.has_perm('equipment.admin_partsuserecordmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 配件字段验证
    def validate_parts(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = PartsInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的配件不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的配件不在--'使用状态'")
        return value


class PartsUseRecordSerialize_Partial(serializers.ModelSerializer):
    """
    配件消耗记录定义--partial
    """

    class Meta:
        model = PartsUseRecordModel
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
        validate_states1(self.instance.state, value)
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = PartsUseRecordModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion


# region 维护记录子项定义 序列化器
class MaintainRecordItemSerialize_Create(serializers.ModelSerializer):
    """
    维护记录子项定义--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MaintainRecordItemModel
        fields = ("id","compoment", "method", "result", "image", "file","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "create_user")


class MaintainRecordItemSerialize_List(serializers.ModelSerializer):
    """
    维护记录子项定义--list
    """
    image = EquipmentImageSerialize_List(many=True)
    file = EquipmentFileSerialize_List(many=True)

    class Meta:
        model = MaintainRecordItemModel
        fields = "__all__"


# endregion
# region 维护信息记录 序列化器
class MaintainRecordSerialize_Create(serializers.ModelSerializer):
    """
    维护信息记录--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MaintainRecordModel
        fields = ("id", "name", "code","type", "state","child", "equipment","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",  "dataTime", "handler", "time_consuming", "image","file","parts_use",
                  "result","desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_maintainrecordmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('equipment.admin_maintainrecordmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = MaintainRecordTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 设备字段验证
    def validate_equipment(self, value):
        list = EquipmentAccountModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的设备不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的设备不在--'使用状态'")
        return value

class MaintainRecordSerialize_List(serializers.ModelSerializer):
    """
    维护信息记录--list
    """
    type = MaintainRecordTypeDefinitionSerialize_List()
    class Meta:
        model = MaintainRecordModel
        fields = ("id", "name", "code","type", "state", "dataTime", "handler", "time_consuming",
                  "result", "auditor", "create_user","create_time","update_time")

class MaintainRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    维护信息记录--retrieve
    """
    file = EquipmentFileSerialize_List(many=True)
    image =EquipmentImageSerialize_List(many=True)
    type = MaintainRecordTypeDefinitionSerialize_List()
    alter = EquipmentAlterRecordSerialize_List(many=True)
    equipment = EquipmentAccountSerialize_List()
    parts_use= PartsUseRecordSerialize_List(many=True)
    child =MaintainRecordItemSerialize_List(many=True)


    class Meta:
        model = MaintainRecordModel
        fields = "__all__"


class MaintainRecordSerialize_Update(serializers.ModelSerializer):
    """
    维护信息记录--update
    """

    class Meta:
        model = MaintainRecordModel
        fields = ("id", "name", "code","type", "child","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",  "equipment", "dataTime", "handler", "time_consuming", "image","file","parts_use",
                  "result","desc", "auditor", )
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
        if not auditor.has_perm('equipment.admin_maintainrecordmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = MaintainRecordTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 设备字段验证
    def validate_equipment(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = EquipmentAccountModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的设备不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的设备不在--'使用状态'")
        return value

class MaintainRecordSerialize_Partial(serializers.ModelSerializer):
    """
    维护信息记录--partial
    """

    class Meta:
        model = MaintainRecordModel
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
        validate_states1(self.instance.state, value)
        if ((self.instance.create_user == self.context['request'].user.username) and\
             (self.instance.auditor != self.context['request'].user.username)):   # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = MaintainRecordModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 设备状态信息 序列化器
class EquipmentStateSerialize_Create(serializers.ModelSerializer):
    """
    设备状态信息--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentStateModel
        fields = ("id", "name", "code","equipment","desc",  "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('equipment.add_equipmentstatemodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        return attrs

     # 设备字段验证
    def validate_equipment(self, value):
        list = EquipmentAccountModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的设备不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的设备不在--'使用状态'")
        return value


class EquipmentStateSerialize_List(serializers.ModelSerializer):
    """
    设备状态信息--list
    """
    equipment = EquipmentAccountSerialize_List()
    class Meta:
        model = EquipmentStateModel
        fields = ("id", "name", "code","type","equipment","runTime","allTime","sum","task", "desc", "create_user","create_time","update_time")


class EquipmentStateSerialize_Retrieve(serializers.ModelSerializer):
    """
    设备状态信息--Retrieve
    """
    equipment = EquipmentAccountSerialize_List()
    class Meta:
        model = EquipmentStateModel
        fields = "__all__"

class EquipmentStateSerialize_Update(serializers.ModelSerializer):
    """
    设备状态信息--update
    """
    class Meta:
        model = EquipmentStateModel
        fields = ("id", "name", "code", "equipment", "desc")

    # 设备字段验证
    def validate_equipment(self, value):
        list = EquipmentAccountModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的设备不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的设备不在--'使用状态'")
        return value

class EquipmentStateSerialize_Partial(serializers.ModelSerializer):
    """
    设备状态信息--partial
    """

    class Meta:
        model = EquipmentStateModel
        fields = ("id","type", "runTime", "allTime","sum","task","util_rate","comp_rate","handler",
                  "attribute1","attribute2","attribute3","attribute4","attribute5","attribute6","attribute7",
                  "attribute8","attribute9","attribute10")

# endregion

