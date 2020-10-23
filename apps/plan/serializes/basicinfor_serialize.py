from rest_framework import serializers
from apps.plan.models.basicinfor_model import *
from apps.process.models.basicinfor_model import *
from apps.quality.models.basicinfor_model import *
from apps.quality.models.recording_model import *
from apps.production.models.basicinfor_model import *
from apps.equipment.models.basicinfor_model import *
from commonFunction import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()

# region  当前APP操作记录 序列化器
class PlanAuditRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP操作记录---list
    """
    class Meta:
        model = PlanAuditRecordModel
        fields = ("id", "uri", "uri_id", "time","classes", "user","result")

class PlanAuditRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    当前APP操作记录---retrieve
    """
    class Meta:
        model = PlanAuditRecordModel
        fields = "__all__"

# endregion

# region  当前APP审核记录 序列化器
class PlanAlterRecordSerialize_Create(serializers.ModelSerializer):
    """
    当前APP审核记录--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PlanAlterRecordModel
        fields = ("id", "uri", "desc","create_user", )

class PlanAlterRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP审核记录---list
    """
    class Meta:
        model = PlanAlterRecordModel
        fields = "__all__"

# endregion

# region  当前APP文件/图片  序列化器
class PlanImageSerialize_Create(serializers.ModelSerializer):
    """
    当前APP图片--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PlanImageModel
        fields = ("id", "image", "uri", "desc","create_user")

    def validate(self, attrs):
        attrs["image_name"]=attrs["image"]
        return attrs

class PlanImageSerialize_List(serializers.ModelSerializer):
    """
    当前APP图片--list
    """
    class Meta:
        model = PlanImageModel
        fields =  "__all__"

class PlanFileSerialize_Create(serializers.ModelSerializer):
    """
    当前APP文件--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PlanFileModel
        fields = ("id", "file", "uri", "desc", "create_user")

    def validate(self, attrs):
        attrs["file_name"] = attrs["file"]
        return attrs

class PlanFileSerialize_List(serializers.ModelSerializer):
    """
    当前APP文件--list
    """
    class Meta:
        model = PlanFileModel
        fields =  "__all__"

# endregion

# region 供应商类型定义 序列化器
class VendorTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    供应商类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = VendorTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_vendortypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_vendortypedefinitionmodel'):
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
                list = VendorTypeDefinitionModel.objects.get(id=value.id)
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


class VendorTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    供应商类型定义--list
    """
    class Meta:
        model = VendorTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class VendorInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    供应商定义--供应商类型定义
    """

    class Meta:
        model = VendorInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class VendorTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    供应商类型定义--retrieve
    """
    file = PlanFileSerialize_List(many=True)                 # 类型文件信息
    alter = PlanAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = VendorTypeDefinitionSerialize_List(required=False)   # 父类别信息
    vendorType_child = VendorTypeDefinitionSerialize_List(many=True)# 子类别信息
    vendorType_item = VendorInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = VendorTypeDefinitionModel
        fields = "__all__"


class VendorTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    供应商类型定义--update
    """
    class Meta:
        model = VendorTypeDefinitionModel
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
        if not auditor.has_perm('plan.admin_vendortypedefinitionmodel'):
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
                list = VendorTypeDefinitionModel.objects.get(id=value.id)
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


class VendorTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    供应商类型定义--partial
    """
    class Meta:
        model = VendorTypeDefinitionModel
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
        obj = VendorTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 供应商类型层级结构 序列化器
class VendorTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    供应商类型层级结构--fourth
    """
    class Meta:
        model = VendorTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class VendorTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    供应商类型定义--third
    """
    vendorType_child = VendorTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = VendorTypeDefinitionModel
        fields = ("id", "name", "code", "state", "vendorType_child")

class VendorTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    供应商类型定义--second
    """
    vendorType_child = VendorTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = VendorTypeDefinitionModel
        fields = ("id", "name", "code", "state", "vendorType_child")

class VendorTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    供应商类型定义--fitst
    """
    vendorType_child = VendorTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = VendorTypeDefinitionModel
        fields = ("id", "name", "code", "state","vendorType_child")

# endregion

# region  供应商信息定义  序列化器
class VendorInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    供应商信息定义 --create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = VendorInforDefinitionModel
        fields = ("id", "name", "code", "state", "type", "image", "file", "address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre", "qualification","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",  "desc", "auditor",
                  "create_user")
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_vendorinfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_vendorinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = VendorTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class VendorInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    供应商信息定义--list
    """
    type =VendorTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = VendorInforDefinitionModel
        fields = ("id", "name", "code","state","type","address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre","auditor","create_user","create_time","update_time")


class VendorInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    供应商信息定义--retrieve
    """
    image = PlanImageSerialize_List(many=True)
    file = PlanFileSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)
    type = VendorTypeDefinitionSerialize_List(required=False)

    class Meta:
        model = VendorInforDefinitionModel
        fields = "__all__"


class VendorInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    供应商信息定义--update
    """

    class Meta:
        model = VendorInforDefinitionModel
        fields = ("id", "name", "code", "type", "image", "file", "address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre", "qualification", "attribute1", "attribute2",
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
        if not auditor.has_perm('plan.admin_vendorinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = VendorTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class VendorInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    供应商信息定义--partial
    """

    class Meta:
        model = VendorInforDefinitionModel
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
        obj = VendorInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 客户类型定义 序列化器
class ClientTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    客户类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ClientTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_clienttypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_clienttypedefinitionmodel'):
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
                list = ClientTypeDefinitionModel.objects.get(id=value.id)
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


class ClientTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    客户类型定义--list
    """
    class Meta:
        model = ClientTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class ClientInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    客户定义--客户类型定义
    """

    class Meta:
        model = ClientInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class ClientTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    客户类型定义--retrieve
    """
    file = PlanFileSerialize_List(many=True)                 # 类型文件信息
    alter = PlanAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = ClientTypeDefinitionSerialize_List(required=False)   # 父类别信息
    clientType_child = ClientTypeDefinitionSerialize_List(many=True)# 子类别信息
    clientType_item = ClientInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = ClientTypeDefinitionModel
        fields = "__all__"


class ClientTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    客户类型定义--update
    """
    class Meta:
        model = ClientTypeDefinitionModel
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
        if not auditor.has_perm('plan.admin_clienttypedefinitionmodel'):
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
                list = ClientTypeDefinitionModel.objects.get(id=value.id)
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


class ClientTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    客户类型定义--partial
    """
    class Meta:
        model = ClientTypeDefinitionModel
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
        obj = ClientTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 客户类型层级结构 序列化器
class ClientTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    客户类型层级结构--fourth
    """
    class Meta:
        model = ClientTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class ClientTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    客户类型定义--third
    """
    clientType_child = ClientTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = ClientTypeDefinitionModel
        fields = ("id", "name", "code", "state", "clientType_child")

class ClientTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    客户类型定义--second
    """
    clientType_child = ClientTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = ClientTypeDefinitionModel
        fields = ("id", "name", "code", "state", "clientType_child")

class ClientTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    客户类型定义--fitst
    """
    clientType_child = ClientTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = ClientTypeDefinitionModel
        fields = ("id", "name", "code", "state","clientType_child")

# endregion

# region  客户信息定义  序列化器
class ClientInforDefinitionSerialize_Create(serializers.ModelSerializer):

    """
    客户信息定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ClientInforDefinitionModel
        fields = ("id", "name", "code","state","type", "image", "file", "address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",  "desc", "auditor","create_user"
                  )
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_clientinfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_clientinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = ClientTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class ClientInforDefinitionSerialize_List(serializers.ModelSerializer):

    """
    客户信息定义--list
    """
    type = ClientTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = ClientInforDefinitionModel
        fields = ("id", "name", "code", "state","type","address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre","auditor","create_user","create_time","update_time")


class ClientInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):

    """
    客户信息定义--retrieve
    """
    image = PlanImageSerialize_List(many=True)
    file = PlanFileSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)
    type = ClientTypeDefinitionSerialize_List(required=False)

    class Meta:
        model = ClientInforDefinitionModel
        fields = "__all__"


class ClientInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    客户信息定义--update
    """

    class Meta:
        model = ClientInforDefinitionModel
        fields = ("id", "name", "code", "type", "image", "file", "address", "mobile",
                  "fax", "wechat", "company_name", "company_abbre","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5",  "desc", "auditor"
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
        if not auditor.has_perm('plan.admin_clientinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = ClientTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class ClientInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    客户信息定义--partial
    """
    class Meta:
        model = ClientInforDefinitionModel
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
        obj = ClientInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 销售子订单创建 序列化器
class SalesOrderItemCreateSerialize_Create(serializers.ModelSerializer):
    """
    销售订单子项创建--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SalesOrderItemCreateModel
        fields =("id","product_id", "batch","state","sum", "file","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","desc","create_user")

    def validate(self, attrs):
        try:
            product = ProductInforDefinitionModel.objects.get(id=attrs["product_id"])  # 判断指定的产品是否存在
        except Exception as e:
            raise serializers.ValidationError("指定的产品不存在")
        attrs["productType_code"] = product.type.code  # 获取产品类型编码
        attrs["productType_name"] = product.type.name  # 获取产品类型名称
        attrs["product_code"] = product.code  # 获取产品编码
        attrs["product_name"] = product.name  # 获取产品名称
        return attrs

class ProductTaskTypeSerialize_ProductTask(serializers.ModelSerializer):
    """
    产品生产任务类型定义--产品生产任务创建
    """
    class Meta:
        model = ProductTaskTypeModel
        fields = ("id", "name", "code", "state", "classes")

class ProductTaskCreateSerialize_ProductTaskItem(serializers.ModelSerializer):
    """
    产品生产任务创建--产品生产任务子项创建--销售订单子项创建
    """
    type=ProductTaskTypeSerialize_ProductTask(required=False)
    class Meta:
        model = ProductTaskCreateModel
        fields = ("id", "name", "code","type","state","update_time",)

class ProductTaskItemCreateSerialize_SalesOrderItem(serializers.ModelSerializer):
    """
    产品生产任务子项创建--销售订单子项创建
    """
    productTaskItem_parent=ProductTaskCreateSerialize_ProductTaskItem(many=True)
    class Meta:
        model = ProductTaskItemCreateModel
        fields = ("id", "state","sum","completed","route_id","update_time","productTaskItem_parent")

class SalesOrderItemCreateSerialize_List(serializers.ModelSerializer):
    """
    销售订单子项创建--list
    """
    file = PlanFileSerialize_List(many=True)
    salesOrderItem_productTaskItem = ProductTaskItemCreateSerialize_SalesOrderItem(many=True)
    class Meta:
        model = SalesOrderItemCreateModel
        fields = "__all__"

class SalesOrderItemCreateSerialize_Partial(serializers.ModelSerializer):
    """
    销售订单子项创建--partial
    """
    class Meta:
        model = SalesOrderCreateModel
        fields = ("id","state")

    # 状态字段验证
    def validate_state(self, value):
        parentState = SalesOrderItemCreateModel.objects.filter(
            id=self.instance.id).first().salesOrderItem_parent.all().values('state')
        if (parentState[0]['state'] != "使用中" ):
            raise serializers.ValidationError("当前订单不处于[使用中状态],禁止更改子项订单状态")
        if not (self.instance.state == "等待" and value == "终止"):
            raise serializers.ValidationError("子订单只能从[等待状态]更改成[终止状态]")
        if not (self.context['request'].user.has_perm('plan.deal_salesordercreatemodel')):
            raise serializers.ValidationError("当前用户不具备执行终止订单权限")
        # 遍历所有管理子订单项的订单项,如果订单项的所有子项都处于END,则将订单设置成END
        data1 = SalesOrderItemCreateModel.objects.filter(id=self.instance.id).first().salesOrderItem_parent.all().values('id')
        for item1 in data1:  # 遍历所有关联此子项的父项
            count = 1
            parentModel = SalesOrderCreateModel.objects.filter(id=item1['id']).first()
            data2=parentModel.child.all().values('id')
            for item2 in data2:  # 遍历父项的所有子项
                child = SalesOrderItemCreateModel.objects.filter(id=item2['id']).first()
                if child.state == "终止":
                    count += 1
                if count ==len(data2):
                   parentModel.state="终止"
                   parentModel.save()
        return value

# endregion

# region 销售订单创建 序列化器
class SalesOrderCreateSerialize_Create(serializers.ModelSerializer):
    """
    销售订单创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SalesOrderCreateModel
        fields =("id", "name", "code", "state", "file", "client", "delivery_time","child","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","desc","auditor","create_user")

     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_salesordercreatemodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        return attrs

    # 客户字段验证
    def validate_client(self, value):
        list = ClientInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 客户否存在
            raise serializers.ValidationError("指定的客户不存在")
        elif (list.state != "使用中"):  # 判断 客户状态是否合适
            raise serializers.ValidationError("指定的客户不在--'使用状态'")
        return value

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('plan.admin_salesordercreatemodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class SalesOrderCreateSerialize_List(serializers.ModelSerializer):
    """
    销售订单创建--list
    """
    client = ClientInforDefinitionSerialize_List()
    class Meta:
        model = SalesOrderCreateModel
        fields = ("id", "name", "code","state","client","delivery_time", "auditor","create_user","create_time","update_time")

class SalesOrderCreateSerialize_Retrieve(serializers.ModelSerializer):
    """
    销售订单创建--retrieve
    """
    file = PlanFileSerialize_List(many=True)
    child = SalesOrderItemCreateSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)
    client = ClientInforDefinitionSerialize_List()

    class Meta:
        model = SalesOrderCreateModel
        fields = "__all__"

class SalesOrderCreateSerialize_Update(serializers.ModelSerializer):
    """
    销售订单创建--update
    """
    class Meta:
        model = SalesOrderCreateModel
        fields = ("id", "name", "code","file", "client", "delivery_time","child" ,"attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","desc", "auditor")
        
     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建': # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return  attrs

    # 客户字段验证
    def validate_client(self, value):
        if self.instance.state != '新建': # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = ClientInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 客户否存在
            raise serializers.ValidationError("指定的客户不存在")
        elif (list.state != "使用中"):  # 判断 客户状态是否合适
            raise serializers.ValidationError("指定的客户不在--'使用状态'")
        return value

    # 审核者字段验证
    def validate_auditor(self, value):
        if self.instance.state != '新建': # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True:
            if self.instance.create_user == value:  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('plan.admin_salesordercreatemodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class SalesOrderCreateSerialize_Partial(serializers.ModelSerializer):
    """
    销售订单创建--partial
    """
    class Meta:
        model = SalesOrderCreateModel
        fields = ("id","state","alter")

    # 所有字段验证
    def validate(self, attrs):
        try:
            del attrs['alter']  # 删除alter字段
        except Exception:
            pass
        return attrs

    # 状态字段验证
    def validate_state(self, value):
        validate_states2(self.instance.state, value)
        if not self.instance.state == "使用中":
            if ((self.instance.create_user == self.context['request'].user.username) and
                    (self.instance.auditor != self.context['request'].user.username)) :  # 如果当前用户为创建账号但不是审核账号
                if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                    raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if value == "使用中":  # 如果新状态为使用中状态
            data=SalesOrderCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有订单子项,并将子项转换成WAIT
                try:
                    child = SalesOrderItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前销售订单项下的子项不存在")
                child.state = "等待"
                child.save()
        if value == "终止": # 如果新状态为终止状态
            if not (self.context['request'].user.has_perm('plan.deal_salesordercreatemodel')):
                raise serializers.ValidationError("当前用户不具备执行订单权限")
            data = SalesOrderCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有订单子项,并将[使用中]的子项转换成END
                try:
                    child = SalesOrderItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前销售订单项下的子项不存在")
                if child.state == "等待":
                    child.state = "终止"
                    child.save()
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = SalesOrderCreateModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion

# region 产品生产任务类型定义 序列化器
class ProductTaskTypeSerialize_Create(serializers.ModelSerializer):
    """
    产品生产任务类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductTaskTypeModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_producttasktypemodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_producttasktypemodel'):
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
                list = ProductTaskTypeModel.objects.get(id=value.id)
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

class ProductTaskTypeSerialize_List(serializers.ModelSerializer):
    """
    产品生产任务类型定义--list
    """
    class Meta:
        model = ProductTaskTypeModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class ProductTaskCreateSerialize_Type(serializers.ModelSerializer):
    """
    产品生产任务定义--产品生产任务类型定义
    """

    class Meta:
        model = ProductTaskCreateModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class ProductTaskTypeSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品生产任务类型定义--retrieve
    """
    file = PlanFileSerialize_List(many=True)                 # 类型文件信息
    alter = PlanAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = ProductTaskTypeSerialize_List(required=False)   # 父类别信息
    productTaskType_child = ProductTaskTypeSerialize_List(many=True)# 子类别信息
    productTaskType_item = ProductTaskCreateSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = ProductTaskTypeModel
        fields = "__all__"


class ProductTaskTypeSerialize_Update(serializers.ModelSerializer):
    """
    产品生产任务类型定义--update
    """
    class Meta:
        model = ProductTaskTypeModel
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
        if not auditor.has_perm('plan.admin_producttasktypemodel'):
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
                list = ProductTaskTypeModel.objects.get(id=value.id)
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


class ProductTaskTypeSerialize_Partial(serializers.ModelSerializer):
    """
    产品生产任务类型定义--partial
    """
    class Meta:
        model = ProductTaskTypeModel
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
        obj = ProductTaskTypeModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 产品生产任务类型层级结构 序列化器
class ProductTaskTypeSerialize_Fourth(serializers.ModelSerializer):
    """
    产品生产任务类型层级结构--fourth
    """
    class Meta:
        model = ProductTaskTypeModel
        fields = ("id", "name", "code", "state")

class ProductTaskTypeSerialize_Third(serializers.ModelSerializer):
    """
    产品生产任务类型定义--third
    """
    productTaskType_child = ProductTaskTypeSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = ProductTaskTypeModel
        fields = ("id", "name", "code", "state", "productTaskType_child")

class ProductTaskTypeSerialize_Second(serializers.ModelSerializer):
    """
    产品生产任务类型定义--second
    """
    productTaskType_child = ProductTaskTypeSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = ProductTaskTypeModel
        fields = ("id", "name", "code", "state", "productTaskType_child")

class ProductTaskTypeSerialize_First(serializers.ModelSerializer):
    """
    产品生产任务类型定义--fitst
    """
    productTaskType_child = ProductTaskTypeSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = ProductTaskTypeModel
        fields = ("id", "name", "code", "state","productTaskType_child")

# endregion

# region 产品生产子任务创建 序列化器
class ProductTaskItemCreateSerialize_Create(serializers.ModelSerializer):
    """
    产品生产任务子项创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductTaskItemCreateModel
        fields = ("id","state", "salesOrderItem","route_id","sum", "file", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user")
        # 所有字段验证
    def validate(self, attrs):
        if 'route_id' in attrs.keys():
            if attrs['route_id'] is not '':
                try:
                    route = ProductRouteDefinitionModel.objects.get(id=attrs["route_id"])  # 判断指定的生产线路是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的生产线路不存在")
                attrs["routeType_code"] = route.type.code  # 获取生产线路类型编码
                attrs["routeType_name"] = route.type.name  # 获取生产线路类型名称
                attrs["route_code"] = route.code  # 获取生产线路编码
                attrs["route_name"] = route.name  # 获取生产线路名称
        return  attrs

    # 订单子项字段验证
    def validate_salesOrderItem(self, value):
        list = SalesOrderItemCreateModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的订单子项不存在")
        elif (list.state != "等待"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的订单子项不在--'等待状态'")
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

class SalesOrderCreateSerialize_ProductTaskItem(serializers.ModelSerializer):
    """
    销售订单创建--销售订单子项创建--产品生产任务子项创建
    """
    class Meta:
        model = SalesOrderCreateModel
        fields = ("id", "name", "code","state")

class SalesOrderItemCreateSerialize_ProductTaskItem(serializers.ModelSerializer):
    """
    销售订单子项创建--产品生产任务子项创建
    """
    salesOrderItem_parent=SalesOrderCreateSerialize_ProductTaskItem(many=True)
    class Meta:
        model = SalesOrderItemCreateModel
        fields = ("id","state","productType_code","productType_name","product_id","product_name","product_code","batch","salesOrderItem_parent")

class ProductTaskItemCreateSerialize_List(serializers.ModelSerializer):
    """
    产品生产任务子项创建--list
    """
    salesOrderItem =SalesOrderItemCreateSerialize_ProductTaskItem()
    class Meta:
        model = ProductTaskItemCreateModel
        fields = "__all__"

class ProductTaskItemCreateSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品生产任务子项创建--Retrieve
    """
    salesOrderItem =SalesOrderItemCreateSerialize_ProductTaskItem()
    productTaskItem_parent=ProductTaskCreateSerialize_ProductTaskItem(many=True)
    class Meta:
        model = ProductTaskItemCreateModel
        fields = "__all__"

class ProductTaskItemCreateSerialize_Partial(serializers.ModelSerializer):
    """
    产品生产任务子项创建--partial
    """

    class Meta:
        model = ProductTaskItemCreateModel
        fields = ("id", "state","completed","attribute1","attribute2","attribute3","attribute4","attribute5","attribute6","attribute7","attribute8","attribute9","attribute10",
              "attribute11", "attribute12", "attribute13", "attribute14", "attribute15", "attribute16", "attribute17",
              "attribute18", "attribute19", "attribute20", )

    # 状态字段验证
    def validate_state(self, value):
        parentState = ProductTaskItemCreateModel.objects.filter(
            id=self.instance.id).first().productTaskItem_parent.all().values('state')
        if (parentState[0]['state'] != "使用中"):
            raise serializers.ValidationError("当前任务不处于[使用中状态],禁止更改任务子项订单状态")
        if not ((self.instance.state == "等待" and (value == "挂起" or value == "加工中" or value == "终止"))or
                (self.instance.state == "挂起" and (value == "等待" or value == "终止")) or
                (self.instance.state == "加工中" and (value == "挂起" or value == "等待" or value == "终止"))):
            raise serializers.ValidationError("子任务不能从"+self.instance.state+"更改成"+value)
        if not (self.context['request'].user.has_perm('plan.deal_producttaskcreatemodel')):
            raise serializers.ValidationError("当前用户不具备执行任务权限")
        if value == "终止":  # 如果新状态为终止状态
            # 遍历所有管理子任务项的任务项,如果任务项的所有子项都处于END,则将任务设置成END
            data1 = ProductTaskItemCreateModel.objects.filter(id=self.instance.id).first().productTaskItem_parent.all().values('id')
            for item1 in data1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = ProductTaskCreateModel.objects.filter(id=item1['id']).first()
                data2 = parentModel.child.all().values('id')
                for item2 in data2:  # 遍历父项的所有子项
                    child = ProductTaskItemCreateModel.objects.filter(id=item2['id']).first()
                    if child.state == "终止":
                        count += 1
                    if count == len(data2):
                        parentModel.state = "终止"
                        parentModel.save()
        return value

    # 完成总数字段验证
    def validate_completed(self, value):
        if not (self.instance.state == "加工中"):
            raise serializers.ValidationError("只有在[加工中状态]下,才能更新加工完成数")
        if value>=self.instance.sum:
            list = SalesOrderItemCreateModel.objects.get(id=self.instance.salesOrderItem_id)
            list.completed+=self.instance.sum
            list.save()
            self.instance.state = "完成"
            data1 =list.salesOrderItem_parent.all().values('id')
            for item1 in data1:  # 遍历与此订单子项相关的订单，判断订单下所有的子订单是否完成
                count = 0
                parentModel = SalesOrderCreateModel.objects.filter(id=item1['id']).first()
                data2 = parentModel.child.all().values('id')
                for item2 in data2:  # 遍历父项的所有子项
                    child = SalesOrderItemCreateModel.objects.filter(id=item2['id']).first()
                    if child.state == "终止":
                        count += 1
                    if child.completed >= child.sum:
                        if child.state == "等待":
                            child.state="完成"
                            child.save()
                        count += 1
                    if count == len(data2):
                        parentModel.state = "完成"
                        parentModel.save()
            # 遍历所有子任务项的任务项,如果任务项的所有子项都处于DONE或END,则将任务设置成DONE
            value1 = ProductTaskItemCreateModel.objects.filter(
                id=self.instance.id).first().productTaskItem_parent.all().values('id')
            for item1 in value1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = ProductTaskCreateModel.objects.filter(id=item1['id']).first()
                value2 = parentModel.child.all().values('id')
                for item2 in value2:  # 遍历父项的所有子项
                    child = ProductTaskItemCreateModel.objects.filter(id=item2['id']).first()
                    if child.state == "终止":
                        count += 1
                    if child.state == "完成":
                        count += 1
                    if count == len(value2):
                        parentModel.state = "完成"
                        parentModel.save()
        return value

# endregion

# region 产品生产任务创建 序列化器
class ProductTaskCreateSerialize_Create(serializers.ModelSerializer):
    """
    产品生产任务创建--create
    """
    state = serializers.HiddenField(default="新建")
    priority = serializers.HiddenField(default="正常")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductTaskCreateModel
        fields = ("id", "name", "code","type", "state", "workshop_code", "priority", "file", "delivery_time", "child", "attribute1", "attribute2",
        "attribute3", "attribute4", "attribute5", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_producttaskcreatemodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        if 'workshop_code' in attrs.keys():
            if attrs['workshop_code'] is not '':
                try:
                    workshop = WorkshopInforDefinitionModel.objects.get(code=attrs["workshop_code"])  # 判断指定的车间务是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的车间不存在")
                attrs["workshop_name"] = workshop.name  # 获取车间名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('plan.admin_producttaskcreatemodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value
    # 类型字段验证
    def validate_type(self, value):
        list = ProductTaskTypeModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class ProductTaskCreateSerialize_List(serializers.ModelSerializer):
    """
    产品生产任务创建--list
    """
    type =ProductTaskTypeSerialize_List(required=False)
    class Meta:
        model = ProductTaskCreateModel
        fields = ("id", "name", "code","type", "state", "priority", "delivery_time", "auditor", "create_user","create_time","update_time")


class ProductTaskCreateSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品生产任务创建--retrieve
    """
    file = PlanFileSerialize_List(many=True)
    child = ProductTaskItemCreateSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)
    type = ProductTaskTypeSerialize_List(required=False)

    class Meta:
        model = ProductTaskCreateModel
        fields = "__all__"


class ProductTaskCreateSerialize_Update(serializers.ModelSerializer):
    """
    产品生产任务创建--update
    """

    class Meta:
        model = ProductTaskCreateModel
        fields = ("id", "name", "code","type", "priority", "file", "delivery_time", "child", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor",)

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

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
        if not auditor.has_perm('plan.admin_producttaskcreatemodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = ProductTaskTypeModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value



class ProductTaskCreateSerialize_Partial(serializers.ModelSerializer):
    """
    产品生产任务创建--partial
    """

    class Meta:
        model = ProductTaskCreateModel
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
        validate_states3(self.instance.state, value)
        if not (self.instance.state == "使用中" or self.instance.state == "挂起" ):
            if (self.instance.create_user == self.context['request'].user.username) and\
            (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
                if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                    raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if value == "审核中":  # 如果新状态为审核状态
            data = ProductTaskCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项,判断分配数量是否超出订单可分配总数
                try:
                    child = ProductTaskItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前产品生产任务项下的子项不存在")
                if child.sum > (child.salesOrderItem.sum-child.salesOrderItem.assigned):
                    raise serializers.ValidationError(child.salesOrderItem.product_name+"项超出订单可分配量")
        if (self.instance.state == "审核中" and  value == "使用中"):  # 如果是由审核状态转换成使用中状态
            data = ProductTaskCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项WAIT,并将关联的销售订单子项分配数量更新
                try:
                    child = ProductTaskItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前产品生产任务项下的子项不存在")
                child.state = "等待"
                child.save()
                child.salesOrderItem.assigned += child.sum
                child.salesOrderItem.save()
        if ((self.instance.state == "挂起" and  value == "使用中") or
            (self.instance.state == "使用中" and  value == "挂起")): # 如果是由挂起状态转与使用中状态互相转换
            if not (self.context['request'].user.has_perm('plan.deal_producttaskcreatemodel')):
                raise serializers.ValidationError("当前用户不具备执行任务权限")
        if value == "终止":  # 如果新状态为终止状态
            if not (self.context['request'].user.has_perm('plan.deal_producttaskcreatemodel')):
                raise serializers.ValidationError("当前用户不具备执行任务权限")
            data = ProductTaskCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项,并将[使用中]的子项转换成END
                try:
                    child = ProductTaskItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前产品生产任务项下的子项不存在")
                if child.state == "等待" or child.state == "挂起":
                    child.state = "终止"
                    child.save()
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = ProductTaskCreateModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value


# endregion

# region 半成品生产任务类型定义 序列化器
class SemifinishedTaskTypeSerialize_Create(serializers.ModelSerializer):
    """
    半成品生产任务类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedTaskTypeModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_semifinishedtasktypemodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_semifinishedtasktypemodel'):
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
                list = SemifinishedTaskTypeModel.objects.get(id=value.id)
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


class SemifinishedTaskTypeSerialize_List(serializers.ModelSerializer):
    """
    半成品生产任务类型定义--list
    """
    class Meta:
        model = SemifinishedTaskTypeModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class SemifinishedTaskCreateSerialize_Type(serializers.ModelSerializer):
    """
    半成品生产任务定义--半成品生产任务类型定义
    """

    class Meta:
        model = SemifinishedTaskCreateModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class SemifinishedTaskTypeSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品生产任务类型定义--retrieve
    """
    file = PlanFileSerialize_List(many=True)                 # 类型文件信息
    alter = PlanAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = SemifinishedTaskTypeSerialize_List(required=False)   # 父类别信息
    semifinishedTaskType_child = SemifinishedTaskTypeSerialize_List(many=True)# 子类别信息
    semifinishedTaskType_item = SemifinishedTaskCreateSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = SemifinishedTaskTypeModel
        fields = "__all__"


class SemifinishedTaskTypeSerialize_Update(serializers.ModelSerializer):
    """
    半成品生产任务类型定义--update
    """
    class Meta:
        model = SemifinishedTaskTypeModel
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
        if not auditor.has_perm('plan.admin_semifinishedtasktypemodel'):
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
                list = SemifinishedTaskTypeModel.objects.get(id=value.id)
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


class SemifinishedTaskTypeSerialize_Partial(serializers.ModelSerializer):
    """
    半成品生产任务类型定义--partial
    """
    class Meta:
        model = SemifinishedTaskTypeModel
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
        obj = SemifinishedTaskTypeModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 半成品生产任务类型层级结构 序列化器
class SemifinishedTaskTypeSerialize_Fourth(serializers.ModelSerializer):
    """
    半成品生产任务类型层级结构--fourth
    """
    class Meta:
        model = SemifinishedTaskTypeModel
        fields = ("id", "name", "code", "state")

class SemifinishedTaskTypeSerialize_Third(serializers.ModelSerializer):
    """
    半成品生产任务类型定义--third
    """
    semifinishedTaskType_child = SemifinishedTaskTypeSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = SemifinishedTaskTypeModel
        fields = ("id", "name", "code", "state", "semifinishedTaskType_child")

class SemifinishedTaskTypeSerialize_Second(serializers.ModelSerializer):
    """
    半成品生产任务类型定义--second
    """
    semifinishedTaskType_child = SemifinishedTaskTypeSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = SemifinishedTaskTypeModel
        fields = ("id", "name", "code", "state", "semifinishedTaskType_child")

class SemifinishedTaskTypeSerialize_First(serializers.ModelSerializer):
    """
    半成品生产任务类型定义--fitst
    """
    semifinishedTaskType_child = SemifinishedTaskTypeSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = SemifinishedTaskTypeModel
        fields = ("id", "name", "code", "state","semifinishedTaskType_child")

# endregion

# region 半成品生产子任务创建 序列化器
class SemifinishedTaskItemCreateSerialize_Create(serializers.ModelSerializer):
    """
    半成品生产任务子项创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedTaskItemCreateModel
        fields = ("id","state",  "semifinished_id", "batch","route_id", "sum", "file", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user")

        def validate(self, attrs):
            if 'route_id' in attrs.keys():
                if attrs['route_id'] is not '':
                    try:
                        route = ProductRouteDefinitionModel.objects.get(id=attrs["route_id"])  # 判断指定的生产线路是否存在
                    except Exception as e:
                        raise serializers.ValidationError("指定的生产线路不存在")
                    attrs["routeType_code"] = route.type.code  # 获取生产线路类型编码
                    attrs["routeType_name"] = route.type.name  # 获取生产线路类型名称
                    attrs["route_code"] = route.code  # 获取生产线路编码
                    attrs["route_name"] = route.name  # 获取生产线路名称
            try:              
                semifinished = SemifinishedInforDefinitionModel.objects.get(id=attrs["semifinished_id"])  # 判断指定的半成品是否存在
            except Exception as e:
                raise serializers.ValidationError("指定的半成品不存在")
            attrs["semifinishedType_code"] = semifinished.type.code  # 获取半成品类型编码
            attrs["semifinishedType_name"] = semifinished.type.name  # 获取半成品类型名称
            attrs["semifinished_code"] = semifinished.code  # 获取半成品编码
            attrs["semifinished_name"] = semifinished.name  # 获取半成品名称
            return attrs

        # 生产线路字段验证
        def validate_route_id(self, value) :
            if len(value) == 0 :
                return value
            if self.instance.state != '新建' :  # 如果不是新建状态 该字段不能更改
                raise serializers.ValidationError("当前信息已提交,禁止更改")
            list = ProductRouteDefinitionModel.objects.get(id=int(value))
            if list is None :  # 判断 父类别是否存在
                raise serializers.ValidationError("指定的生产线路不存在")
            elif (list.state != "使用中") :  # 判断 父类别状态是否合适
                raise serializers.ValidationError("指定的生产线路不在--'使用状态'")
            return value

class SemifinishedTaskItemCreateSerialize_List(serializers.ModelSerializer):
    """
    半成品生产任务子项创建--list
    """
    class Meta:
        model = SemifinishedTaskItemCreateModel
        fields = "__all__"

class SemifinishedTaskCreateSerialize_SemifinishedTaskItem(serializers.ModelSerializer):
    """
    半成品生产任务创建--半成品生产任务子项创建
    """
    type = SemifinishedTaskTypeSerialize_List(required=False)
    class Meta:
        model = SemifinishedTaskCreateModel
        fields = ("id", "name", "code","type", "state", "priority", "delivery_time",)

class SemifinishedTaskItemCreateSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品生产任务子项创建--Retrieve
    """
    semifinishedTaskItem_parent=SemifinishedTaskCreateSerialize_SemifinishedTaskItem(many=True)
    class Meta:
        model = SemifinishedTaskItemCreateModel
        fields = "__all__"

class SemifinishedTaskItemCreateSerialize_Partial(serializers.ModelSerializer):
    """
    半成品生产任务子项创建--partial
    """

    class Meta:
        model = SemifinishedTaskItemCreateModel
        fields = (
        "id", "state", "completed", "attribute1", "attribute2", "attribute3", "attribute4", "attribute5", "attribute6",
        "attribute7", "attribute8", "attribute9", "attribute10","attribute11", "attribute12", "attribute13", "attribute14",
        "attribute15", "attribute16", "attribute17", "attribute18", "attribute19", "attribute20",)

    # 状态字段验证
    def validate_state(self, value):
        parentState = SemifinishedTaskItemCreateModel.objects.filter(
            id=self.instance.id).first().SemifinishedTaskItem_parent.all().values('state')
        if (parentState[0]['state'] != "使用中"):
            raise serializers.ValidationError("当前任务不处于[使用中状态],禁止更改子项任务状态")
        if not ((self.instance.state == "等待" and (value == "挂起" or value == "加工中" or value == "终止"))or
                (self.instance.state == "挂起" and (value == "等待" or value == "终止")) or
                (self.instance.state == "加工中" and (value == "挂起" or value == "等待" or value == "终止"))):
            raise serializers.ValidationError("子任务不能从"+self.instance.state+"更改成"+value)
        if not (self.context['request'].user.has_perm('plan.deal_semifinishedtaskcreatemodel')):
            raise serializers.ValidationError("当前用户不具备执行任务权限")
        return value

    # 完成总数字段验证
    def validate_completed(self, value):
        if not (self.instance.state == "加工中"):
            raise serializers.ValidationError("只有在[加工中状态]下,才能更新加工完成数")
            # 遍历所有子任务项的任务项,如果任务项的所有子项都处于DONE或END,则将任务设置成DONE
            value1 = SemifinishedTaskItemCreateModel.objects.filter(
                id=self.instance.id).first().semifinishedTaskItem_parent.all().values('id')
            for item1 in value1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = SemifinishedTaskCreateModel.objects.filter(id=item1['id']).first()
                value2 = parentModel.child.all().values('id')
                for item2 in value2:  # 遍历父项的所有子项
                    child = SemifinishedTaskItemCreateModel.objects.filter(id=item2['id']).first()
                    if child.state == "终止":
                        count += 1
                    if child.state == "完成":
                        count += 1
                    if count == len(value2):
                        parentModel.state = "完成"
                        parentModel.save()
        return value

# endregion

# region 半成品生产任务创建 序列化器
class SemifinishedTaskCreateSerialize_Create(serializers.ModelSerializer):
    """
    半成品生产任务创建--create
    """
    state = serializers.HiddenField(default="新建")
    priority = serializers.HiddenField(default="正常")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedTaskCreateModel
        fields = ("id", "name", "code","type", "state", "workshop_code", "priority", "file", "delivery_time", "child", "attribute1", "attribute2",
        "attribute3", "attribute4", "attribute5", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_semifinishedtaskcreatemodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        if 'workshop_code' in attrs.keys():
            if attrs['workshop_code'] is not '':
                try:
                    workshop = WorkshopInforDefinitionModel.objects.get(code=attrs["workshop_code"])  # 判断指定的车间务是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的车间不存在")
                attrs["workshop_name"] = workshop.name  # 获取车间名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('plan.admin_semifinishedtaskcreatemodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = SemifinishedTaskTypeModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class SemifinishedTaskCreateSerialize_List(serializers.ModelSerializer):
    """
    半成品生产任务创建--list
    """
    type = SemifinishedTaskTypeSerialize_List(required=False)
    class Meta:
        model = SemifinishedTaskCreateModel
        fields = ("id", "name", "code","type", "state", "priority", "delivery_time", "auditor", "create_user","create_time","update_time")


class SemifinishedTaskCreateSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品生产任务创建--retrieve
    """
    file = PlanFileSerialize_List(many=True)
    child = SemifinishedTaskItemCreateSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)
    type = SemifinishedTaskTypeSerialize_List(required=False)

    class Meta:
        model = SemifinishedTaskCreateModel
        fields = "__all__"


class SemifinishedTaskCreateSerialize_Update(serializers.ModelSerializer):
    """
    半成品生产任务创建--update
    """

    class Meta:
        model = SemifinishedTaskCreateModel
        fields = ("id", "name", "code", "type","priority", "file", "delivery_time", "child", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor",)

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

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
        if not auditor.has_perm('plan.admin_semifinishedtaskcreatemodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = SemifinishedTaskTypeModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class SemifinishedTaskCreateSerialize_Partial(serializers.ModelSerializer):
    """
    半成品生产任务创建--partial
    """

    class Meta:
        model = SemifinishedTaskCreateModel
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
        validate_states3(self.instance.state, value)
        if not (self.instance.state == "使用中" or self.instance.state == "挂起" ):
            if (self.instance.create_user == self.context['request'].user.username) and\
           (self.instance.auditor != self.context['request'].user.username):  # 如果当前用户为创建账号但不是审核账号
                if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                    raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if value == "审核中":  # 如果新状态为审核状态
            data = SemifinishedTaskCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项,判断分配数量是否超出订单可分配总数
                try:
                    SemifinishedTaskItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前半成品生产任务项下的子项不存在")
        if (self.instance.state == "审核中" and  value == "使用中"):  # 如果是由审核状态转换成使用中状态
            data = SemifinishedTaskCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项WAIT,并将关联的销售订单子项分配数量更新
                try:
                    child = SemifinishedTaskItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前半成品生产任务项下的子项不存在")
                child.state = "等待"
                child.save()
                child.salesOrderItem.assigned += child.sum
                child.salesOrderItem.save()
        if ((self.instance.state == "挂起" and  value == "使用中") or
            (self.instance.state == "使用中" and  value == "挂起")): # 如果是由挂起状态转与使用中状态互相转换
            if not (self.context['request'].user.has_perm('plan.deal_semifinishedtaskcreatemodel')):
                raise serializers.ValidationError("当前用户不具备执行任务权限")
        if value == "终止":  # 如果新状态为终止状态
            if not (self.context['request'].user.has_perm('plan.deal_semifinishedtaskcreatemodel')):
                raise serializers.ValidationError("当前用户不具备执行任务权限")
            data = SemifinishedTaskCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项,并将[使用中]的子项转换成END
                try:
                    child = SemifinishedTaskItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前半成品生产任务项下的子项不存在")
                if child.state == "等待" or child.state == "挂起":
                    child.state = "终止"
                    child.save()
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = SemifinishedTaskCreateModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value


# endregion

# region 采购需求单子项创建 序列化器
class PurchaseRequireItemCreateSerialize_Create(serializers.ModelSerializer):
    """
    采购需求单子项创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PurchaseRequireItemCreateModel
        fields = ("id", "state", "material_id","sum", "vendor","file","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc","create_user")

    def validate(self, attrs):
        try:
            material = MaterialInforDefinitionModel.objects.get(id=attrs["material_id"])  # 判断指定的物料是否存在
        except Exception as e:
            raise serializers.ValidationError("指定的物料不存在")
        attrs["materialType_code"] = material.type.code  # 获取物料类型编码
        attrs["materialType_name"] = material.type.name  # 获取物料类型名称
        attrs["material_code"] = material.code  # 获取物料编码
        attrs["material_name"] = material.name  # 获取物料名称
        return attrs

    # 供应商字段验证
    def validate_vendor(self, value):
        list = VendorInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 供应商否存在
            raise serializers.ValidationError("指定的供应商不存在")
        elif (list.state != "使用中"):  # 判断 客户状态是否合适
            raise serializers.ValidationError("指定的供应商不在--'使用状态'")
        return value


class PurchaseRequireItemCreateSerialize_List(serializers.ModelSerializer):
    """
    采购需求单子项创建--list
    """
    file = PlanFileSerialize_List(many=True)
    vendor = VendorInforDefinitionSerialize_List()

    class Meta:
        model = PurchaseRequireItemCreateModel
        fields = "__all__"

class PurchaseRequireItemCreateSerialize_Partial(serializers.ModelSerializer):
    """
    采购需求单子项创建--partial
    """
    class Meta:
        model = SalesOrderCreateModel
        fields = ("id","state")

    # 状态字段验证
    def validate_state(self, value):
        parentState = PurchaseRequireItemCreateModel.objects.filter(
            id=self.instance.id).first().purchaseRequireItem_parent.all().values('state')
        if (parentState[0]['state'] != "使用中" ):
            raise serializers.ValidationError("当前采购需求单不处于[使用中状态],禁止更改子项需求单状态")
        if not (self.instance.state == "等待" and (value == "终止" or value == "完成")):
            raise serializers.ValidationError("子需求单只能从[等待状态]更改成[终止状态]或[完成状态]")
        if not (self.context['request'].user.has_perm('plan.deal_purchaserequirecreatemodel')):
            raise serializers.ValidationError("当前用户不具备执行终止需求单权限")
        # 遍历所有管理子需求单项的订单项,如果需求单项的所有子项都处于END,则将需求单设置成END
        data1 = PurchaseRequireItemCreateModel.objects.filter(id=self.instance.id).first().purchaseRequireItem_parent.all().values('id')
        if (value == "终止"):
            for item1 in data1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = PurchaseRequireCreateModel.objects.filter(id=item1['id']).first()
                data2=parentModel.child.all().values('id')
                for item2 in data2:  # 遍历父项的所有子项
                    child = PurchaseRequireItemCreateModel.objects.filter(id=item2['id']).first()
                    if child.state == "终止":
                        count += 1
                    if count ==len(data2):
                       parentModel.state="终止"
                       parentModel.save()
        if (value == "完成"):
            for item1 in data1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = PurchaseRequireCreateModel.objects.filter(id=item1['id']).first()
                data2=parentModel.child.all().values('id')
                for item2 in data2:  # 遍历父项的所有子项
                    child = PurchaseRequireItemCreateModel.objects.filter(id=item2['id']).first()
                    if (child.state == "终止" or child.state == "完成"):
                        count += 1
                    if count ==len(data2):
                       parentModel.state="完成"
                       parentModel.save()
        return value
# endregion

# region 采购需求单创建 序列化器
class PurchaseRequireCreateSerialize_Create(serializers.ModelSerializer):
    """
    采购需求单创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PurchaseRequireCreateModel
        fields = ("id", "name", "code", "state", "child", "dataTime", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "file","desc", "auditor","create_user")

     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_purchaserequirecreatemodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_purchaserequirecreatemodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class PurchaseRequireCreateSerialize_List(serializers.ModelSerializer):
    """
    采购需求单创建--list
    """

    class Meta:
        model = PurchaseRequireCreateModel
        fields = ("id", "name", "code", "state", "auditor","create_user","create_time","update_time")

class PurchaseRequireCreateSerialize_Retrieve(serializers.ModelSerializer):
    """
    采购需求单创建--retrieve
    """
    file = PlanFileSerialize_List(many=True)
    child =PurchaseRequireItemCreateSerialize_List()
    alter = PlanAlterRecordSerialize_List(many=True)

    class Meta:
        model = PurchaseRequireCreateModel
        fields = "__all__"

class PurchaseRequireCreateSerialize_Update(serializers.ModelSerializer):
    """
    采购需求单创建--update
    """
    class Meta:
        model = PurchaseRequireCreateModel
        fields = ("id", "name", "code", "child", "dataTime", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "file", "desc", "auditor")

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建': # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return  attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        if self.instance.state != '新建': # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True:
            if self.instance.create_user == value:  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('plan.admin_purchaserequirecreatemodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class PurchaseRequireCreateSerialize_Partial(serializers.ModelSerializer):
    """
    采购需求单创建--partial
    """
    class Meta:
        model = PurchaseRequireCreateModel
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
        validate_states4(self.instance.state, value)
        if not self.instance.state == "使用中":
            if self.instance.create_user == self.context['request'].user.username:  # 如果当前用户为创建
                if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                    raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if value == "使用中":  # 如果新状态为使用中状态
            data = PurchaseRequireCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有订单子项,并将子项转换成WAIT
                try:
                    child = PurchaseRequireItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前采购需求项下的子项不存在")
                child.state = "等待"
                child.save()
        if value == "终止":  # 如果新状态为终止状态
            if not (self.context['request'].user.has_perm('plan.deal_purchaserequirecreatemodel')):
                raise serializers.ValidationError("当前用户不具备执行终止采购单权限")
            data = PurchaseRequireCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有采购单子项,并将[等待中]的子项转换成[终止]
                try:
                    child = PurchaseRequireItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前采购需求单下的子项不存在")
                if child.state == "等待":
                    child.state = "终止"
                    child.save()
        if value == "完成":  # 如果新状态为完成状态
            if not (self.context['request'].user.has_perm('plan.deal_purchaserequirecreatemodel')):
                raise serializers.ValidationError("当前用户不具备执行采购单权限")
            data = PurchaseRequireCreateModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有采购单子项,并将[等待中]的子项转换成[完成]
                try:
                    child = PurchaseRequireItemCreateModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前采购需求单下的子项不存在")
                if child.state == "等待":
                    child.state = "完成"
                    child.save()
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = PurchaseRequireCreateModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion

# region 物料管理计划子项创建 序列化器
class MaterialManagePlanItemSerialize_Create(serializers.ModelSerializer):
    """
    物料管理计划子项创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MaterialManagePlanItemModel
        fields =("id","type", "state","material_id", "sum", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","desc","create_user")

    def validate(self, attrs):
        try:
            material = MaterialInforDefinitionModel.objects.get(id=attrs["material_id"])  # 判断指定的物料是否存在
        except Exception as e:
            raise serializers.ValidationError("指定的物料不存在")
        if material.state != "使用中":
            raise serializers.ValidationError("指定的物料不在'使用中'状态")
        attrs["materialType_code"] = material.type.code  # 获取物料类型编码
        attrs["materialType_name"] = material.type.name  # 获取物料类型名称
        attrs["material_code"] = material.code  # 获取物料编码
        attrs["material_name"] = material.name  # 获取物料名称
        return attrs


class MaterialManagePlanItemSerialize_List(serializers.ModelSerializer):
    """
    物料管理计划子项创建--list
    """

    class Meta:
        model = MaterialManagePlanItemModel
        fields = "__all__"

class MaterialManagePlanItemSerialize_Partial(serializers.ModelSerializer):
    """
    物料管理计划子项创建--partial
    """
    class Meta:
        model = MaterialManagePlanItemModel
        fields = ("id", "state","completed")

    # 状态字段验证
    def validate_state(self, value):
        parentState = MaterialManagePlanItemModel.objects.filter(
            id=self.instance.id).first().materialManageItem_parent.all().values('state')
        if (parentState[0]['state'] != "使用中"):
            raise serializers.ValidationError("当前任务不处于[使用中状态],禁止更改子项任务状态")
        if not (self.instance.state == "等待" and value == "终止"):
            raise serializers.ValidationError("子任务只能从[等待状态]更改成[终止状态]")
        if not (self.context['request'].user.has_perm('plan.deal_materialmanageplanmodel')):
            raise serializers.ValidationError("当前用户不具备执行任务权限")
        # 遍历所有管理子任务项的任务项,如果任务项的所有子项都处于END,则将任务设置成END
        data1 = MaterialManagePlanItemModel.objects.filter(id=self.instance.id).first().materialManageItem_parent.all().values('id')
        for item1 in data1:  # 遍历所有关联此子项的父项
            count = 1
            parentModel = MaterialManagePlanModel.objects.filter(id=item1['id']).first()
            data2 = parentModel.child.all().values('id')
            for item2 in data2:  # 遍历父项的所有子项
                child = MaterialManagePlanItemModel.objects.filter(id=item2['id']).first()
                if child.state == "终止":
                    count += 1
                if count == len(data2):
                    parentModel.state = "终止"
                    parentModel.save()
        return value

    # 完成总数字段验证
    def validate_completed(self, value):
        if not (self.instance.state == "等待"):
            raise serializers.ValidationError("只有在[等待]状态下,才能更新计划完成数")
        if value>=self.instance.sum:
            self.instance.state = "完成"
            # 遍历所有子任务项的任务项,如果任务项的所有子项都处于DONE或END,则将任务设置成DONE
            value1 = MaterialManagePlanItemModel.objects.filter(
                id=self.instance.id).first().materialManageItem_parent.all().values('id')
            for item1 in value1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = MaterialManagePlanModel.objects.filter(id=item1['id']).first()
                value2 = parentModel.child.all().values('id')
                for item2 in value2:  # 遍历父项的所有子项
                    child = MaterialManagePlanItemModel.objects.filter(id=item2['id']).first()
                    if (child.state == "终止" or child.state == "完成"):
                        count += 1
                    if count == len(value2):
                        parentModel.state = "完成"
                        parentModel.save()
        return value


# endregion

# region 物料管理计划创建 序列化器
class MaterialManagePlanSerialize_Create(serializers.ModelSerializer):
    """
    物料管理计划创建--create
    """
    state = serializers.HiddenField(default="新建")
    priority = serializers.HiddenField(default="正常")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MaterialManagePlanModel
        fields = ("id", "name", "code", "state", "priority", "child","dataTime", "file", "desc","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_materialmanageplanmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_materialmanageplanmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class MaterialManagePlanSerialize_List(serializers.ModelSerializer):
    """
    物料管理计划创建--list
    """

    class Meta:
        model = MaterialManagePlanModel
        fields = ("id", "name", "code", "state", "priority", "dataTime", "auditor", "create_user","create_time","update_time")


class MaterialManagePlanSerialize_Retrieve(serializers.ModelSerializer):
    """
    物料管理计划创建--retrieve
    """
    file = PlanFileSerialize_List(many=True)
    child = MaterialManagePlanItemSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)

    class Meta:
        model = MaterialManagePlanModel
        fields = "__all__"


class MaterialManagePlanSerialize_Update(serializers.ModelSerializer):
    """
    物料管理计划创建--update
    """
    class Meta:
        model = MaterialManagePlanModel
        fields = ("id", "name", "code","child", "priority","dataTime","file","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor")

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

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
        if not auditor.has_perm('plan.admin_materialmanageplanmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

class MaterialManagePlanSerialize_Partial(serializers.ModelSerializer):
    """
    物料管理计划创建--partial
    """

    class Meta:
        model = MaterialManagePlanModel
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
        validate_states3(self.instance.state, value)
        if not self.instance.state == "使用中":
            if self.instance.create_user == self.context['request'].user.username:  # 如果当前用户为创建
                if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                    raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "审核中" and value == "使用中"):  # 如果是由审核状态转换成使用中状态
            data = MaterialManagePlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项WAIT
                try:
                    child = MaterialManagePlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前任务项下的子项不存在")
                child.state = "等待"
                child.save()
        if ((self.instance.state == "挂起" and value == "使用中") or
                (self.instance.state == "使用中" and value == "挂起")):  # 如果是由挂起状态转与使用中状态互相转换
            if not (self.context['request'].user.has_perm('plan.deal_materialmanageplanmodel')):
                raise serializers.ValidationError("当前用户不具备执行任务权限")
        if value == "终止":  # 如果新状态为终止状态
            if not (self.context['request'].user.has_perm('plan.deal_materialmanageplanmodel')):
                raise serializers.ValidationError("当前用户不具备执行订单权限")
            data = MaterialManagePlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有订单子项,并将[使用中]的子项转换成END
                try:
                    child = MaterialManagePlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前任务项下的子项不存在")
                if child.state == "等待":
                    child.state = "终止"
                    child.save()
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = MaterialManagePlanModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 半成品管理计划子项创建 序列化器
class SemifinishedManagePlanItemSerialize_Create(serializers.ModelSerializer):
    """
    半成品管理计划子项创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedManagePlanItemModel
        fields = ("id", "type", "state", "semifinished_id", "sum", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user")

    def validate(self, attrs):
        try:
            semifinished = SemifinishedInforDefinitionModel.objects.get(id=attrs["semifinished_id"])  # 判断指定的半成品是否存在
        except Exception as e:
            raise serializers.ValidationError("指定的半成品不存在")
        if semifinished.state != "使用中":
            raise serializers.ValidationError("指定的半成品不在'使用中'状态")
        attrs["semifinishedType_code"] = semifinished.type.code  # 获取半成品类型编码
        attrs["semifinishedType_name"] = semifinished.type.name  # 获取半成品类型名称
        attrs["semifinished_code"] = semifinished.code  # 获取半成品编码
        attrs["semifinished_name"] = semifinished.name  # 获取半成品名称
        return attrs


class SemifinishedManagePlanItemSerialize_List(serializers.ModelSerializer):
    """
    半成品管理计划子项创建--list
    """

    class Meta:
        model = SemifinishedManagePlanItemModel
        fields = "__all__"


class SemifinishedManagePlanItemSerialize_Partial(serializers.ModelSerializer):
    """
    半成品管理计划子项创建--partial
    """

    class Meta:
        model = SemifinishedManagePlanItemModel
        fields = ("id", "state", "completed")

    # 状态字段验证
    def validate_state(self, value):
        parentState = SemifinishedManagePlanItemModel.objects.filter(
            id=self.instance.id).first().semifinishedManageItem_parent.all().values('state')
        if (parentState[0]['state'] != "使用中"):
            raise serializers.ValidationError("当前任务不处于[使用中状态],禁止更改子项任务状态")
        if not (self.instance.state == "等待" and value == "终止"):
            raise serializers.ValidationError("子任务只能从[等待状态]更改成[终止状态]")
        if not (self.context['request'].user.has_perm('plan.deal_semifinishedmanageplanmodel')):
            raise serializers.ValidationError("当前用户不具备执行任务权限")
        # 遍历所有管理子任务项的任务项,如果任务项的所有子项都处于END,则将任务设置成END
        data1 = SemifinishedManagePlanItemModel.objects.filter(
            id=self.instance.id).first().semifinishedManageItem_parent.all().values('id')
        for item1 in data1:  # 遍历所有关联此子项的父项
            count = 1
            parentModel = SemifinishedManagePlanModel.objects.filter(id=item1['id']).first()
            data2 = parentModel.child.all().values('id')
            for item2 in data2:  # 遍历父项的所有子项
                child = SemifinishedManagePlanItemModel.objects.filter(id=item2['id']).first()
                if child.state == "终止":
                    count += 1
                if count == len(data2):
                    parentModel.state = "终止"
                    parentModel.save()
        return value

    # 完成总数字段验证
    def validate_completed(self, value):
        if not (self.instance.state == "等待"):
            raise serializers.ValidationError("只有在[等待]状态下,才能更新计划完成数")
        if value >= self.instance.sum:
            self.instance.state = "完成"
            # 遍历所有子任务项的任务项,如果任务项的所有子项都处于DONE或END,则将任务设置成DONE
            value1 = SemifinishedManagePlanItemModel.objects.filter(
                id=self.instance.id).first().semifinishedManageItem_parent.all().values('id')
            for item1 in value1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = SemifinishedManagePlanModel.objects.filter(id=item1['id']).first()
                value2 = parentModel.child.all().values('id')
                for item2 in value2:  # 遍历父项的所有子项
                    child = SemifinishedManagePlanItemModel.objects.filter(id=item2['id']).first()
                    if (child.state == "终止" or child.state == "完成"):
                        count += 1
                    if count == len(value2):
                        parentModel.state = "完成"
                        parentModel.save()
        return value


# endregion

# region 半成品管理计划创建 序列化器
class SemifinishedManagePlanSerialize_Create(serializers.ModelSerializer):
    """
    半成品管理计划创建--create
    """
    state = serializers.HiddenField(default="新建")
    priority = serializers.HiddenField(default="正常")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedManagePlanModel
        fields = (
        "id", "name", "code", "state", "priority", "child", "dataTime", "file", "desc", "attribute1", "attribute2",
        "attribute3", "attribute4", "attribute5", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_semifinishedmanageplanmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_semifinishedmanageplanmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class SemifinishedManagePlanSerialize_List(serializers.ModelSerializer):
    """
    半成品管理计划创建--list
    """

    class Meta:
        model = SemifinishedManagePlanModel
        fields = ("id", "name", "code", "state", "priority", "dataTime", "auditor", "create_user","create_time","update_time")


class SemifinishedManagePlanSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品管理计划创建--retrieve
    """
    file = PlanFileSerialize_List(many=True)
    child = SemifinishedManagePlanItemSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)

    class Meta:
        model = SemifinishedManagePlanModel
        fields = "__all__"


class SemifinishedManagePlanSerialize_Update(serializers.ModelSerializer):
    """
    半成品管理计划创建--update
    """

    class Meta:
        model = SemifinishedManagePlanModel
        fields = ("id", "name", "code", "child", "priority", "dataTime", "file", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor")

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

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
        if not auditor.has_perm('plan.admin_semifinishedmanageplanmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class SemifinishedManagePlanSerialize_Partial(serializers.ModelSerializer):
    """
    半成品管理计划创建--partial
    """

    class Meta:
        model = SemifinishedManagePlanModel
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
        validate_states3(self.instance.state, value)
        if not self.instance.state == "使用中":
            if self.instance.create_user == self.context['request'].user.username:  # 如果当前用户为创建
                if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                    raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "审核中" and value == "使用中"):  # 如果是由审核状态转换成使用中状态
            data = SemifinishedManagePlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项WAIT
                try:
                    child = SemifinishedManagePlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前任务项下的子项不存在")
                child.state = "等待"
                child.save()
        if ((self.instance.state == "挂起" and value == "使用中") or
                (self.instance.state == "使用中" and value == "挂起")):  # 如果是由挂起状态转与使用中状态互相转换
            if not (self.context['request'].user.has_perm('plan.deal_semifinishedmanageplanmodel')):
                raise serializers.ValidationError("当前用户不具备执行任务权限")
        if value == "终止":  # 如果新状态为终止状态
            if not (self.context['request'].user.has_perm('plan.deal_semifinishedmanageplanmodel')):
                raise serializers.ValidationError("当前用户不具备执行订单权限")
            data = SemifinishedManagePlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有订单子项,并将[使用中]的子项转换成END
                try:
                    child = SemifinishedManagePlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前任务项下的子项不存在")
                if child.state == "等待":
                    child.state = "终止"
                    child.save()
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = SemifinishedManagePlanModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 产品管理计划子项创建 序列化器
class ProductManagePlanItemSerialize_Create(serializers.ModelSerializer):
    """
    产品管理计划子项创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductManagePlanItemModel
        fields = ("id", "type", "state", "product_id", "sum", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user")

    def validate(self, attrs):
        try:
            product = ProductInforDefinitionModel.objects.get(id=attrs["product_id"])  # 判断指定的产品是否存在
        except Exception as e:
            raise serializers.ValidationError("指定的产品不存在")
        if product.state != "使用中":
            raise serializers.ValidationError("指定的产品不在'使用中'状态")
        attrs["productType_code"] = product.type.code  # 获取产品类型编码
        attrs["productType_name"] = product.type.name  # 获取产品类型名称
        attrs["product_code"] = product.code  # 获取产品编码
        attrs["product_name"] = product.name  # 获取产品名称
        return attrs


class ProductManagePlanItemSerialize_List(serializers.ModelSerializer):
    """
    产品管理计划子项创建--list
    """

    class Meta:
        model = ProductManagePlanItemModel
        fields = "__all__"


class ProductManagePlanItemSerialize_Partial(serializers.ModelSerializer):
    """
    产品管理计划子项创建--partial
    """

    class Meta:
        model = ProductManagePlanItemModel
        fields = ("id", "state", "completed")

    # 状态字段验证
    def validate_state(self, value):
        parentState = ProductManagePlanItemModel.objects.filter(
            id=self.instance.id).first().productManageItem_parent.all().values('state')
        if (parentState[0]['state'] != "使用中"):
            raise serializers.ValidationError("当前任务不处于[使用中状态],禁止更改子项任务状态")
        if not (self.instance.state == "等待" and value == "终止"):
            raise serializers.ValidationError("子任务只能从[等待状态]更改成[终止状态]")
        if not (self.context['request'].user.has_perm('plan.deal_productmanageplanmodel')):
            raise serializers.ValidationError("当前用户不具备执行任务权限")
        # 遍历所有管理子任务项的任务项,如果任务项的所有子项都处于END,则将任务设置成END
        data1 = ProductManagePlanItemModel.objects.filter(
            id=self.instance.id).first().productManageItem_parent.all().values('id')
        for item1 in data1:  # 遍历所有关联此子项的父项
            count = 1
            parentModel = ProductManagePlanModel.objects.filter(id=item1['id']).first()
            data2 = parentModel.child.all().values('id')
            for item2 in data2:  # 遍历父项的所有子项
                child = ProductManagePlanItemModel.objects.filter(id=item2['id']).first()
                if child.state == "终止":
                    count += 1
                if count == len(data2):
                    parentModel.state = "终止"
                    parentModel.save()
        return value

    # 完成总数字段验证
    def validate_completed(self, value):
        if not (self.instance.state == "等待"):
            raise serializers.ValidationError("只有在[等待]状态下,才能更新计划完成数")
        if value >= self.instance.sum:
            self.instance.state = "完成"
            # 遍历所有子任务项的任务项,如果任务项的所有子项都处于DONE或END,则将任务设置成DONE
            value1 = ProductManagePlanItemModel.objects.filter(
                id=self.instance.id).first().productManageItem_parent.all().values('id')
            for item1 in value1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = ProductManagePlanModel.objects.filter(id=item1['id']).first()
                value2 = parentModel.child.all().values('id')
                for item2 in value2:  # 遍历父项的所有子项
                    child = ProductManagePlanItemModel.objects.filter(id=item2['id']).first()
                    if (child.state == "终止" or child.state == "完成"):
                        count += 1
                    if count == len(value2):
                        parentModel.state = "完成"
                        parentModel.save()
        return value


# endregion

# region 产品管理计划创建 序列化器
class ProductManagePlanSerialize_Create(serializers.ModelSerializer):
    """
    产品管理计划创建--create
    """
    state = serializers.HiddenField(default="新建")
    priority = serializers.HiddenField(default="正常")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductManagePlanModel
        fields = (
        "id", "name", "code", "state", "priority", "child", "dataTime", "file", "desc", "attribute1", "attribute2",
        "attribute3", "attribute4", "attribute5", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_productmanageplanmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_productmanageplanmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class ProductManagePlanSerialize_List(serializers.ModelSerializer):
    """
    产品管理计划创建--list
    """

    class Meta:
        model = ProductManagePlanModel
        fields = ("id", "name", "code", "state", "priority", "dataTime", "auditor", "create_user","create_time","update_time")


class ProductManagePlanSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品管理计划创建--retrieve
    """
    file = PlanFileSerialize_List(many=True)
    child = ProductManagePlanItemSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)

    class Meta:
        model = ProductManagePlanModel
        fields = "__all__"


class ProductManagePlanSerialize_Update(serializers.ModelSerializer):
    """
    产品管理计划创建--update
    """

    class Meta:
        model = ProductManagePlanModel
        fields = ("id", "name", "code", "child", "priority", "dataTime", "file", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor")

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

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
        if not auditor.has_perm('plan.admin_productmanageplanmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class ProductManagePlanSerialize_Partial(serializers.ModelSerializer):
    """
    产品管理计划创建--partial
    """

    class Meta:
        model = ProductManagePlanModel
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
        validate_states3(self.instance.state, value)
        if not self.instance.state == "使用中":
            if self.instance.create_user == self.context['request'].user.username:  # 如果当前用户为创建
                if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                    raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "审核中" and value == "使用中"):  # 如果是由审核状态转换成使用中状态
            data = ProductManagePlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有任务子项WAIT
                try:
                    child = ProductManagePlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前任务项下的子项不存在")
                child.state = "等待"
                child.save()
        if ((self.instance.state == "挂起" and value == "使用中") or
                (self.instance.state == "使用中" and value == "挂起")):  # 如果是由挂起状态转与使用中状态互相转换
            if not (self.context['request'].user.has_perm('plan.deal_productmanageplanmodel')):
                raise serializers.ValidationError("当前用户不具备执行任务权限")
        if value == "终止":  # 如果新状态为终止状态
            if not (self.context['request'].user.has_perm('plan.deal_productmanageplanmodel')):
                raise serializers.ValidationError("当前用户不具备执行订单权限")
            data = ProductManagePlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有订单子项,并将[使用中]的子项转换成END
                try:
                    child = ProductManagePlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前任务项下的子项不存在")
                if child.state == "等待":
                    child.state = "终止"
                    child.save()
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = ProductManagePlanModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 设备维护计划子项创建 序列化器
class EquipmentMaintainPlanItemSerialize_Create(serializers.ModelSerializer):
    """
    设备维护计划子项创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = EquipmentMaintainPlanItemModel
        fields = ("id","state","equipment_id", "handler","consuming_time","file", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","desc", "create_user")

    def validate(self, attrs):
        try:
            equipment = EquipmentAccountModel.objects.get(id=attrs["equipment_id"])  # 判断指定的设备是否存在
        except Exception as e:
            raise serializers.ValidationError("指定的设备不存在")
        if equipment.state!="使用中":
            raise serializers.ValidationError("指定的设备不在'使用中'状态")
        attrs["equipmentType_code"] = equipment.type.code  # 获取设备类型编码
        attrs["equipmentType_name"] = equipment.type.name  # 获取设备类型名称
        attrs["equipment_code"] = equipment.code  # 获取设备编码
        attrs["equipment_name"] = equipment.name  # 获取设备名称
        return attrs


class EquipmentMaintainPlanItemSerialize_List(serializers.ModelSerializer):
    """
    设备维护计划子项创建--list
    """
    file = PlanFileSerialize_List(many=True)

    class Meta:
        model = EquipmentMaintainPlanItemModel
        fields = "__all__"

class EquipmentMaintainPlanItemSerialize_Partial(serializers.ModelSerializer):
    """
    设备维护计划子项创建--partial
    """
    class Meta:
        model = EquipmentMaintainPlanItemModel
        fields = ("id","state")

    # 状态字段验证
    def validate_state(self, value):
        parentState = EquipmentMaintainPlanItemModel.objects.filter(
            id=self.instance.id).first().equipmentMaintainPlanItem_parent.all().values('state')
        if (parentState[0]['state'] != "使用中" ):
            raise serializers.ValidationError("当前设备维护计划单不处于[使用中状态],禁止更改子项维护计划单状态")
        if not (self.instance.state == "等待" and (value == "终止" or value == "完成")):
            raise serializers.ValidationError("子维护计划单只能从[等待状态]更改成[终止状态]或[完成状态]")
        if not (self.context['request'].user.has_perm('plan.deal_equipmentmaintainplanmodel')):
            raise serializers.ValidationError("当前用户不具备执行终止维护计划单权限")
        # 遍历所有管理子维护计划单项的订单项,如果维护计划单项的所有子项都处于END,则将维护计划单设置成END
        data1 = EquipmentMaintainPlanItemModel.objects.filter(id=self.instance.id).first().equipmentMaintainPlanItem_parent.all().values('id')
        if (value == "终止"):
            for item1 in data1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = EquipmentMaintainPlanModel.objects.filter(id=item1['id']).first()
                data2=parentModel.child.all().values('id')
                for item2 in data2:  # 遍历父项的所有子项
                    child = EquipmentMaintainPlanItemModel.objects.filter(id=item2['id']).first()
                    if child.state == "终止":
                        count += 1
                    if count ==len(data2):
                       parentModel.state="终止"
                       parentModel.save()
        if (value == "完成"):
            for item1 in data1:  # 遍历所有关联此子项的父项
                count = 1
                parentModel = EquipmentMaintainPlanModel.objects.filter(id=item1['id']).first()
                data2=parentModel.child.all().values('id')
                for item2 in data2:  # 遍历父项的所有子项
                    child = EquipmentMaintainPlanItemModel.objects.filter(id=item2['id']).first()
                    if (child.state == "终止" or child.state == "完成"):
                        count += 1
                    if count ==len(data2):
                       parentModel.state="完成"
                       parentModel.save()
        return value
# endregion

# region 设备维护计划创建 序列化器
class EquipmentMaintainPlanSerialize_Create(serializers.ModelSerializer):
    """
    设备维护计划创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = EquipmentMaintainPlanModel
        fields = ("id", "name", "code", "state", "child", "dataTime","file", "desc","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_equipmentmaintainplanmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_equipmentmaintainplanmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

class EquipmentMaintainPlanSerialize_List(serializers.ModelSerializer):
    """
    设备维护计划创建--list
    """

    class Meta:
        model = EquipmentMaintainPlanModel
        fields = ("id", "name", "code", "state", "dataTime","auditor", "create_user","create_time","update_time")


class EquipmentMaintainPlanSerialize_Retrieve(serializers.ModelSerializer):
    """
    设备维护计划创建--retrieve
    """
    file = PlanFileSerialize_List(many=True)
    child = EquipmentMaintainPlanItemSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)

    class Meta:
        model = EquipmentMaintainPlanModel
        fields = "__all__"


class EquipmentMaintainPlanSerialize_Update(serializers.ModelSerializer):
    """
    设备维护计划创建--update
    """

    class Meta:
        model = EquipmentMaintainPlanModel
        fields = ("id", "name", "code", "child", "dataTime","file", "desc","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","auditor",)

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs


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
        if not auditor.has_perm('plan.admin_equipmentmaintainplanmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class EquipmentMaintainPlanSerialize_Partial(serializers.ModelSerializer):
    """
    设备维护计划创建--partial
    """

    class Meta:
        model = EquipmentMaintainPlanModel
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
        validate_states4(self.instance.state, value)
        if not self.instance.state == "使用中":
            if self.instance.create_user == self.context['request'].user.username:  # 如果当前用户为创建
                if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                    raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if value == "使用中":  # 如果新状态为使用中状态
            data = EquipmentMaintainPlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有计划单子项,并将子项转换成WAIT
                try:
                    child = EquipmentMaintainPlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前设备维护计划下的子项不存在")
                child.state = "等待"
                child.save()
        if value == "终止":  # 如果新状态为终止状态
            if not (self.context['request'].user.has_perm('plan.deal_equipmentmaintainplanmodel')):
                raise serializers.ValidationError("当前用户不具备执行终止采购单权限")
            data = EquipmentMaintainPlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有采购单子项,并将[等待中]的子项转换成[终止]
                try:
                    child = EquipmentMaintainPlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前设备维护计划单下的子项不存在")
                if child.state == "等待":
                    child.state = "终止"
                    child.save()
        if value == "完成":  # 如果新状态为完成状态
            if not (self.context['request'].user.has_perm('plan.deal_equipmentmaintainplanmodel')):
                raise serializers.ValidationError("当前用户不具备执行采购单权限")
            data = EquipmentMaintainPlanModel.objects.filter(id=self.instance.id).first().child.all().values('id')
            for item in data:  # 遍历所有采购单子项,并将[等待中]的子项转换成[完成]
                try:
                    child = EquipmentMaintainPlanItemModel.objects.get(id=item['id'])
                except Exception as e:
                    raise serializers.ValidationError("当前设备维护计划单下的子项不存在")
                if child.state == "等待":
                    child.state = "完成"
                    child.save()
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = PlanBoardModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion

# region  计划看板定义  序列化器
class PlanBoardSerialize_Create(serializers.ModelSerializer):

    """
    计划看板定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = PlanBoardModel
        fields = ("id", "name", "code","state", "image", "file","desc", "auditor","create_user"
                  )
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('plan.add_planboardmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('plan.admin_planboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class  PlanBoardSerialize_List(serializers.ModelSerializer):

    """
    计划看板定义--list
    """
    image = PlanImageSerialize_List()
    class Meta:
        model = PlanBoardModel
        fields = ("id", "name", "code", "state","image","create_user","auditor","create_time","update_time")


class PlanBoardSerialize_Retrieve(serializers.ModelSerializer):

    """
    计划看板定义--retrieve
    """
    image = PlanImageSerialize_List()
    file =PlanFileSerialize_List(many=True)
    alter = PlanAlterRecordSerialize_List(many=True)
    class Meta:
        model = PlanBoardModel
        fields = "__all__"


class PlanBoardSerialize_Update(serializers.ModelSerializer):
    """
    计划看板定义--update
    """

    class Meta:
        model = PlanBoardModel
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
        if not auditor.has_perm('plan.admin_planboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class PlanBoardSerialize_Partial(serializers.ModelSerializer):
    """
    计划看板定义--partial
    """

    class Meta:
        model = PlanBoardModel
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
        obj = PlanBoardModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion