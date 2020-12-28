from rest_framework import serializers
from apps.warehouse.models.basicinfor_model import *
from commonFunction import *
from django.contrib.auth import get_user_model

from Mes import settings
User= get_user_model()

# region  当前APP操作记录 序列化器
class WarehouseAuditRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP操作记录---list
    """
    class Meta:
        model = WarehouseAuditRecordModel
        fields = ("id", "uri", "uri_id", "time","classes", "user","result")

class WarehouseAuditRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    当前APP操作记录---retrieve
    """
    class Meta:
        model = WarehouseAuditRecordModel
        fields = "__all__"

# endregion

# region  当前APP审核记录 序列化器
class WarehouseAlterRecordSerialize_Create(serializers.ModelSerializer):
    """
    当前APP审核记录--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WarehouseAlterRecordModel
        fields = ("id", "uri", "desc","create_user", )

class WarehouseAlterRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP审核记录---list
    """
    class Meta:
        model = WarehouseAlterRecordModel
        fields = "__all__"

# endregion

# region  当前APP文件/图片  序列化器
class WarehouseImageSerialize_Create(serializers.ModelSerializer):
    """
    当前APP图片--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WarehouseImageModel
        fields = ("id", "image", "uri", "desc","create_user")

    def validate(self, attrs):
        attrs["image_name"]=attrs["image"]
        return attrs

class WarehouseImageSerialize_List(serializers.ModelSerializer):
    """
    当前APP图片--list
    """
    class Meta:
        model = WarehouseImageModel
        fields =  "__all__"

class WarehouseFileSerialize_Create(serializers.ModelSerializer):
    """
    当前APP文件--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WarehouseFileModel
        fields = ("id", "file", "uri", "desc", "create_user")

    def validate(self, attrs):
        attrs["file_name"] = attrs["file"]
        return attrs

class WarehouseFileSerialize_List(serializers.ModelSerializer):
    """
    当前APP文件--list
    """
    class Meta:
        model = WarehouseFileModel
        fields =  "__all__"

# endregion

# region  仓库信息定义 序列化器
class WarehouseDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    仓库信息定义---create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WarehouseDefinitionModel
        fields = ("id", "name", "code","state","type", "classes", "parent", "position_sum", "image",
                  "affiliation", "location", "principal", "desc","attach_attribute","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "file", "auditor","create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('warehouse.add_warehousedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('warehouse.admin_warehousedefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 父类别字段验证
    def validate_parent(self, value):
        if self.initial_data['classes']=="一级类别":   # 判断 父类别是否为一级类别
            if value != None:                    # 一级类别不能指定父类别
                raise serializers.ValidationError("处于[一级类别]的信息不能指定父类别")
        else:
            if value is None:                     # 非一级类别必须指定父类别
                raise serializers.ValidationError("处于"+self.initial_data["classes"]+"级别的信息必须指定父类别")
            else:               # 判断指定的父类别是否符合条件
                list=WarehouseDefinitionModel.objects.get(id=value.id)
                if list is None:                         # 判断 父类别是否存在
                    raise serializers.ValidationError("指定的父仓库不存在")
                elif(list.state!="使用中"):               # 判断 父类别状态是否合适
                    raise serializers.ValidationError("指定的父类别不在--'使用中'状态")
                else:                                    # 判断  子父类别的层级是否合适
                    if self.initial_data['classes'] == "二级类别" and  list.classes!= "一级类别":
                        raise serializers.ValidationError("[二级类别]的父类别必须是[一级类别]'")
                    if self.initial_data['classes'] == "三级类别" and list.classes != "二级类别":
                        raise serializers.ValidationError("[三级类别]的父类别必须是[二级类别]")
                    if self.initial_data['classes'] == "四级类别" and list.classes != "三级类别":
                        raise serializers.ValidationError("[四级类别]的父类别必须是[三级类别]")
        return value

class WarehouseDefinitionSerialize_List(serializers.ModelSerializer):
    """
    仓库信息定义---list
    """
    class Meta:
        model = WarehouseDefinitionModel
        fields = ("id", "name", "code", "state","position_sum","type", "classes","auditor","create_user","create_time","update_time")

class PositionDefinitionSerialize_Warehouse(serializers.ModelSerializer):
    """
    仓位信息定义---仓库信息定义
    """
    class Meta:
        model = PositionDefinitionModel
        fields = ("id", "name", "code", "state", "maximum", "auditor","create_user")

class WarehouseDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    仓库信息定义---retrieve
    """
    image = WarehouseImageSerialize_List(many=True)
    file = WarehouseFileSerialize_List(many=True)
    alter = WarehouseAlterRecordSerialize_List(many=True)
    parent = WarehouseDefinitionSerialize_List(required=False)
    warehouse_child=WarehouseDefinitionSerialize_List(many=True)
    warehouse_item = PositionDefinitionSerialize_Warehouse(many=True)

    class Meta:
        model = WarehouseDefinitionModel
        fields = "__all__"


class WarehouseDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    仓库信息定义---update
    """

    class Meta:
        model = WarehouseDefinitionModel
        fields = ("id", "name", "code", "type","classes", "parent", "image","attach_attribute", "file", "position_sum",
                  "affiliation", "location", "principal","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor",)

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
        if not auditor.has_perm('warehouse.admin_warehousedefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 父类别字段验证
    def validate_parent(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if self.initial_data['classes']=="一级类别":   # 判断 父类别是否为一级类别
            if value != None:                    # 一级类别不能指定父类别
                raise serializers.ValidationError("处于[一级类别]的信息不能指定父类别")
        else:
            if value is None:                     # 非一级类别必须指定父类别
                raise serializers.ValidationError("处于"+self.initial_data["classes"]+"级别的信息必须指定父类别")
            else:               # 判断指定的父类别是否符合条件
                list=WarehouseDefinitionModel.objects.get(id=value.id)
                if list is None:                         # 判断 父类别是否存在
                    raise serializers.ValidationError("指定的父仓库不存在")
                elif(list.state!="使用中"):               # 判断 父类别状态是否合适
                    raise serializers.ValidationError("指定的父类别不在--'使用中'状态")
                else:                                    # 判断  子父类别的层级是否合适
                    if self.initial_data['classes'] == "二级类别" and  list.classes!= "一级类别":
                        raise serializers.ValidationError("[二级类别]的父类别必须是[一级类别]'")
                    if self.initial_data['classes'] == "三级类别" and list.classes != "二级类别":
                        raise serializers.ValidationError("[三级类别]的父类别必须是[二级类别]")
                    if self.initial_data['classes'] == "四级类别" and list.classes != "三级类别":
                        raise serializers.ValidationError("[四级类别]的父类别必须是[三级类别]")
        return value
class WarehouseDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    仓库信息定义---partial
    """

    class Meta:
        model = WarehouseDefinitionModel
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
        obj = WarehouseDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion

# region 仓库层级结构 序列化器
class WarehouseDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    仓库层级结构--fourth
    """
    class Meta:
        model = WarehouseDefinitionModel
        fields = ("id", "name", "code", "state")

class WarehouseDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    仓库定义--third
    """
    warehouse_child = WarehouseDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = WarehouseDefinitionModel
        fields = ("id", "name", "code", "state", "warehouse_child")

class WarehouseDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    仓库定义--second
    """
    warehouse_child = WarehouseDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = WarehouseDefinitionModel
        fields = ("id", "name", "code", "state", "warehouse_child")

class WarehouseDefinitionSerialize_First(serializers.ModelSerializer):
    """
    仓库定义--fitst
    """
    warehouse_child = WarehouseDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = WarehouseDefinitionModel
        fields = ("id", "name", "code", "state","warehouse_child")

# endregion

# region  仓位信息定义 序列化器
class PositionDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    仓位信息定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PositionDefinitionModel
        fields = ("id", "name", "code","state", "type", "maximum", "place", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "image", "file", "desc",
                  "auditor","create_user")
   # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('warehouse.add_positiondefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('warehouse.admin_positiondefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 父仓库字段验证
    def validate_type(self, value):
        list = WarehouseDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的仓库不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的仓库不在--'使用状态'")
        return value

class PositionDefinitionSerialize_List(serializers.ModelSerializer):
    """
    仓位信息定义---list
    """
    type = WarehouseDefinitionSerialize_List()
    class Meta:
        model = PositionDefinitionModel
        fields = ("id", "name", "code", "state","type","place","maximum", "auditor","create_user","create_time","update_time")

class PositionDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    仓位信息定义---retrieve
    """
    image = WarehouseImageSerialize_List(many=True)
    file = WarehouseFileSerialize_List(many=True)
    alter = WarehouseAlterRecordSerialize_List(many=True)
    type = WarehouseDefinitionSerialize_List()
    class Meta:
        model = PositionDefinitionModel
        fields = "__all__"

class PositionDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    仓位信息定义--update
    """

    class Meta:
        model = PositionDefinitionModel
        fields = ("id", "name", "code","type", "image", "file", "maximum", "place", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor")

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
        if not auditor.has_perm('warehouse.admin_positiondefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = WarehouseDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的仓库不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的仓库不在--'使用状态'")
        return value

class PositionDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    仓位信息定义--partial
    """

    class Meta:
        model = PositionDefinitionModel
        fields = ("id","state","alter")

    # 所有字段验证
    def validate(self, attrs):
        try:
            del attrs['alter']  # 删除alter字段
        except Exception:
            pass
        if attrs['state']=="审核中":
            condtions = {'state__in': ("审核中","使用中", "闲置"),
                         'type__code__iexact':self.instance.type.code}
            positionNum=PositionDefinitionModel.objects.filter(**condtions).count()
            if (positionNum >= self.instance.type.position_sum):
                raise serializers.ValidationError("提交的仓位数超过了仓库最大仓位数限制")
        return attrs

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = PositionDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

    def validate_state(self, value):
        if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "新建" and \
                ( value == "审核中" or value == "作废")):
            return value
        if (self.instance.state == "审核中") and(
                 value == "新建" or value == "闲置" or value == "作废"):
            return value
        if (self.instance.state == "闲置") and \
                (value == "使用中" or value == "作废"):
            return value
        if (self.instance.state == "使用中" and \
                ( value == "闲置")):
            return value
        raise serializers.ValidationError("不能从" + self.instance.state + "更新到" + value)
        return value
# endregion

# region  仓库看板定义  序列化器
class WarehouseBoardSerialize_Create(serializers.ModelSerializer):

    """
    仓库看板定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = WarehouseBoardModel
        fields = ("id", "name", "code","state", "image", "file","desc", "auditor","create_user"
                  )
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('warehouse.add_warehouseboardmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('warehouse.admin_warehouseboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class  WarehouseBoardSerialize_List(serializers.ModelSerializer):

    """
    仓库看板定义--list
    """
    image = WarehouseImageSerialize_List()
    class Meta:
        model = WarehouseBoardModel
        fields = ("id", "name", "code", "state","image","create_user","auditor","create_time","update_time")


class WarehouseBoardSerialize_Retrieve(serializers.ModelSerializer):

    """
    仓库看板定义--retrieve
    """
    image = WarehouseImageSerialize_List()
    file =WarehouseFileSerialize_List(many=True)
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta:
        model = WarehouseBoardModel
        fields = "__all__"


class WarehouseBoardSerialize_Update(serializers.ModelSerializer):
    """
    仓库看板定义--update
    """

    class Meta:
        model = WarehouseBoardModel
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
        if not auditor.has_perm('warehouse.admin_warehouseboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class WarehouseBoardSerialize_Partial(serializers.ModelSerializer):
    """
    仓库看板定义--partial
    """

    class Meta:
        model = WarehouseBoardModel
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
        obj = WarehouseBoardModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion