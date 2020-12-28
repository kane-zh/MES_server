from rest_framework import serializers
from apps.quality.models.basicinfor_model import *
from apps.quality.models.recording_model import *
from commonFunction import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()

# region  当前APP操作记录 序列化器
class QualityAuditRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP操作记录---list
    """
    class Meta:
        model = QualityAuditRecordModel
        fields = ("id", "uri", "uri_id", "time","classes", "user","result")

class QualityAuditRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    当前APP操作记录---retrieve
    """
    class Meta:
        model = QualityAuditRecordModel
        fields = "__all__"

# endregion

# region  当前APP审核记录 序列化器
class QualityAlterRecordSerialize_Create(serializers.ModelSerializer):
    """
    当前APP审核记录--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = QualityAlterRecordModel
        fields = ("id", "uri", "desc","create_user", )

class QualityAlterRecordSerialize_List(serializers.ModelSerializer):
    """
    当前APP审核记录---list
    """
    class Meta:
        model = QualityAlterRecordModel
        fields = "__all__"

# endregion

# region  当前APP文件/图片  序列化器
class QualityImageSerialize_Create(serializers.ModelSerializer):
    """
    当前APP图片--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = QualityImageModel
        fields = ("id", "image", "uri", "desc","create_user")

    def validate(self, attrs):
        attrs["image_name"]=attrs["image"]
        return attrs

class QualityImageSerialize_List(serializers.ModelSerializer):
    """
    当前APP图片--list
    """
    class Meta:
        model = QualityImageModel
        fields =  "__all__"

class QualityFileSerialize_Create(serializers.ModelSerializer):
    """
    当前APP文件--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = QualityFileModel
        fields = ("id", "file", "uri", "desc", "create_user")

    def validate(self, attrs):
        attrs["file_name"] = attrs["file"]
        return attrs

class QualityFileSerialize_List(serializers.ModelSerializer):
    """
    当前APP文件--list
    """
    class Meta:
        model = QualityFileModel
        fields =  "__all__"

# endregion

# region 缺陷类型定义 序列化器
class DefectTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    缺陷类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DefectTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('quality.add_defecttypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('quality.admin_defecttypedefinitionmodel'):
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
                list = DefectTypeDefinitionModel.objects.get(id=value.id)
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


class DefectTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    缺陷类型定义--list
    """
    class Meta:
        model = DefectTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class DefectInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    缺陷定义--缺陷类型定义
    """

    class Meta:
        model = DefectInforDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class DefectTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    缺陷类型定义--retrieve
    """
    file = QualityFileSerialize_List(many=True)                 # 类型文件信息
    alter = QualityAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = DefectTypeDefinitionSerialize_List(required=False)   # 父类别信息
    defectType_child = DefectTypeDefinitionSerialize_List(many=True)# 子类别信息
    defectType_item = DefectInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = DefectTypeDefinitionModel
        fields = "__all__"


class DefectTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    缺陷类型定义--update
    """
    class Meta:
        model = DefectTypeDefinitionModel
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
        if not auditor.has_perm('quality.admin_defecttypedefinitionmodel'):
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
                list = DefectTypeDefinitionModel.objects.get(id=value.id)
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


class DefectTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    缺陷类型定义--partial
    """
    class Meta:
        model = DefectTypeDefinitionModel
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
        obj = DefectTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 缺陷类型层级结构 序列化器
class DefectTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    缺陷类型层级结构--fourth
    """
    class Meta:
        model = DefectTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class DefectTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    缺陷类型层级结构--third
    """
    defectType_child = DefectTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = DefectTypeDefinitionModel
        fields = ("id", "name", "code", "state", "defectType_child")

class DefectTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    缺陷类型层级结构--second
    """
    defectType_child = DefectTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = DefectTypeDefinitionModel
        fields = ("id", "name", "code", "state", "defectType_child")

class DefectTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    缺陷类型层级结构--fitst
    """
    defectType_child = DefectTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = DefectTypeDefinitionModel
        fields = ("id", "name", "code", "state","defectType_child")

# endregion

# region 缺陷等级定义 序列化器
class DefectGradeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    缺陷等级定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DefectGradeDefinitionModel
        fields = ("id", "name", "code", "state", "rule", "influences", "processing_method",
                   "file", "attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5","desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('quality.add_defectgradedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('quality.admin_defectgradedefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class DefectGradeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    缺陷等级定义--list
    """

    class Meta:
        model = DefectGradeDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user","create_time","update_time")

class DefectInforDefinitionSerialize_Grade(serializers.ModelSerializer):
    """
    缺陷定义--缺陷等级
    """
    type = DefectTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = DefectInforDefinitionModel
        fields = ("id", "name", "code", "state","type","auditor","create_user")

class DefectGradeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    缺陷等级定义--retrieve
    """
    file = QualityFileSerialize_List(many=True)
    alter = QualityAlterRecordSerialize_List(many=True)
    defectGrade_defectInfor = DefectInforDefinitionSerialize_Grade(many=True)

    class Meta:
        model = DefectGradeDefinitionModel
        fields = "__all__"


class DefectGradeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    缺陷等级定义--update
    """

    class Meta:
        model = DefectGradeDefinitionModel
        fields = ("id", "name", "code", "rule", "influences", "processing_method",
                   "file","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "auditor")
    # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止创建者更改")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止创建者更改")
        if settings.SAME_USER != True:
            if self.instance.create_user == value:  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('quality.admin_defectgradedefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class DefectGradeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    缺陷等级定义--partial
    """

    class Meta:
        model = DefectGradeDefinitionModel
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
        obj = DefectGradeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 缺陷定义 序列化器
class DefectInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    缺陷定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = DefectInforDefinitionModel
        fields = ("id","name", "code","state", "type","defect_grade","rule", "attribute1", "attribute2",
                      "attribute3", "attribute4","attribute5",  "file","image", "desc", "auditor","create_user")

     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('quality.add_defectinfordefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('quality.admin_defectinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = DefectTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class DefectInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    缺陷定义--list
    """
    type = DefectTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = DefectInforDefinitionModel
        fields = ("id", "name", "code", "state","type","auditor","create_user","create_time","update_time")

class DefectInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    缺陷定义--retrieve
    """
    image =QualityImageSerialize_List(many=True)
    file = QualityFileSerialize_List(many=True)
    alter = QualityAlterRecordSerialize_List(many=True)
    type = DefectTypeDefinitionSerialize_List(required=False)
    defect_grade=DefectGradeDefinitionSerialize_List(required=False)

    class Meta:
        model = DefectInforDefinitionModel
        fields = "__all__"

class DefectInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    缺陷定义--update
    """
    class Meta:
        model = DefectInforDefinitionModel
        fields = ("id", "name", "code","type","defect_grade","rule", "attribute1", "attribute2",
                      "attribute3", "attribute4","attribute5",  "file","image", "desc", "auditor")

     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止创建者更改")
        return  attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止创建者更改")
        if settings.SAME_USER != True:
            if self.instance.create_user == value:  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('quality.admin_defectinfordefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = DefectTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class DefectInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    缺陷定义--partial
    """
    class Meta:
        model = DefectInforDefinitionModel
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
        obj = DefectInforDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 检验标准类型定义 序列化器
class InspectionStandardTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    检验标准类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InspectionStandardTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('quality.add_inspectionstandardtypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('quality.admin_inspectionstandardtypedefinitionmodel'):
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
                list = InspectionStandardTypeDefinitionModel.objects.get(id=value.id)
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


class InspectionStandardTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    检验标准类型定义--list
    """
    class Meta:
        model = InspectionStandardTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class InspectionStandardInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    检验标准定义--检验标准类型定义
    """

    class Meta:
        model = InspectionStandardDefinitionModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class InspectionStandardTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    检验标准类型定义--retrieve
    """
    file = QualityFileSerialize_List(many=True)                 # 类型文件信息
    alter = QualityAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = InspectionStandardTypeDefinitionSerialize_List(required=False)   # 父类别信息
    inspectionStandardType_child = InspectionStandardTypeDefinitionSerialize_List(many=True)# 子类别信息
    inspectionStandardType_item = InspectionStandardInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = InspectionStandardTypeDefinitionModel
        fields = "__all__"


class InspectionStandardTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    检验标准类型定义--update
    """
    class Meta:
        model = InspectionStandardTypeDefinitionModel
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
        if not auditor.has_perm('quality.admin_inspectionstandardtypedefinitionmodel'):
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
                list = InspectionStandardTypeDefinitionModel.objects.get(id=value.id)
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


class InspectionStandardTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    检验标准类型定义--partial
    """
    class Meta:
        model = InspectionStandardTypeDefinitionModel
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
        obj = InspectionStandardTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 检验标准类型层级结构 序列化器
class InspectionStandardTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    检验标准类型层级结构--fourth
    """
    class Meta:
        model = InspectionStandardTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class InspectionStandardTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    检验标准类型层级结构--third
    """
    inspectionStandardType_child = InspectionStandardTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = InspectionStandardTypeDefinitionModel
        fields = ("id", "name", "code", "state", "inspectionStandardType_child")

class InspectionStandardTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    检验标准类型层级结构--second
    """
    inspectionStandardType_child = InspectionStandardTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = InspectionStandardTypeDefinitionModel
        fields = ("id", "name", "code", "state", "inspectionStandardType_child")

class InspectionStandardTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    检验标准类型层级结构--fitst
    """
    inspectionStandardType_child = InspectionStandardTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = InspectionStandardTypeDefinitionModel
        fields = ("id", "name", "code", "state","inspectionStandardType_child")

# endregion

# region 检验标准定义 序列化器
class InspectionStandardsDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    检验标准定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InspectionStandardDefinitionModel
        fields = ("id", "name", "code","state", "type", "defect","samples_ration","ok_ration","ng_ration","concession_ration",
                  "attribute1", "attribute2","attribute3", "attribute4","attribute5", "file", "desc", "auditor","create_user")
     # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('quality.add_inspectionstandarddefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('quality.admin_inspectionstandarddefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = InspectionStandardTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class InspectionStandardsDefinitionSerialize_List(serializers.ModelSerializer):
    """
    检验标准定义--list
    """
    type = InspectionStandardTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = InspectionStandardDefinitionModel
        fields = ("id", "name", "code", "state","type","auditor","create_user","create_time","update_time"
                  )

class InspectionStandardsDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    检验标准定义--retrieve
    """
    file = QualityFileSerialize_List(many=True)
    alter = QualityAlterRecordSerialize_List(many=True)
    type = InspectionStandardTypeDefinitionSerialize_List(required=False)
    defect = DefectInforDefinitionSerialize_List(many=True)

    class Meta:
        model = InspectionStandardDefinitionModel
        fields = "__all__"

class InspectionStandardsDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    检验标准定义--update
    """
    class Meta:
        model = InspectionStandardDefinitionModel
        fields = ("id", "name", "code", "type", "defect", "samples_ration","ok_ration","ng_ration","concession_ration",
                  "attribute1", "attribute2", "attribute3", "attribute4", "attribute5", "file", "desc", "auditor")
     # 所有字段验证
    def validate(self, attrs):
        if self.instance.state != '新建':  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止创建者更改")
        return  attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止创建者更改")
        if settings.SAME_USER != True:
            if self.instance.create_user == value:  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('quality.admin_inspectionstandarddefinitionmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = InspectionStandardTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class InspectionStandardsDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    检验标准定义--partial
    """
    class Meta:
        model = InspectionStandardDefinitionModel
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
        obj = InspectionStandardDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion

# region 检验汇报类型定义 序列化器
class InspectionReportTypeDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    检验汇报类型定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InspectionReportTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "parent", "attach_attribute",
                  "file", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('quality.add_inspectionreporttypedefinitionmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('quality.admin_inspectionreporttypedefinitionmodel'):
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
                list = InspectionReportTypeDefinitionModel.objects.get(id=value.id)
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


class InspectionReportTypeDefinitionSerialize_List(serializers.ModelSerializer):
    """
    检验汇报类型定义--list
    """
    class Meta:
        model = InspectionReportTypeDefinitionModel
        fields = ("id", "name", "code", "state", "classes", "auditor", "create_user","create_time","update_time")


class InspectionReportInforDefinitionSerialize_Type(serializers.ModelSerializer):
    """
    检验汇报定义--检验汇报类型定义
    """

    class Meta:
        model = InspectionReportModel
        fields = ("id", "name", "code", "state", "auditor", "create_user")

class InspectionReportTypeDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    检验汇报类型定义--retrieve
    """
    file = QualityFileSerialize_List(many=True)                 # 类型文件信息
    alter = QualityAlterRecordSerialize_List(many=True)         # 审核记录信息
    parent = InspectionReportTypeDefinitionSerialize_List(required=False)   # 父类别信息
    inspectionReportType_child = InspectionReportTypeDefinitionSerialize_List(many=True)# 子类别信息
    inspectionReportType_item = InspectionReportInforDefinitionSerialize_Type(many=True)# 附属项信息

    class Meta:
        model = InspectionReportTypeDefinitionModel
        fields = "__all__"


class InspectionReportTypeDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    检验汇报类型定义--update
    """
    class Meta:
        model = InspectionReportTypeDefinitionModel
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
        if not auditor.has_perm('quality.admin_inspectionreporttypedefinitionmodel'):
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
                list = InspectionReportTypeDefinitionModel.objects.get(id=value.id)
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


class InspectionReportTypeDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    检验汇报类型定义--partial
    """
    class Meta:
        model = InspectionReportTypeDefinitionModel
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
        obj = InspectionReportTypeDefinitionModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion

# region 检验汇报类型层级结构 序列化器
class InspectionReportTypeDefinitionSerialize_Fourth(serializers.ModelSerializer):
    """
    检验汇报类型层级结构--fourth
    """
    class Meta:
        model = InspectionReportTypeDefinitionModel
        fields = ("id", "name", "code", "state")

class InspectionReportTypeDefinitionSerialize_Third(serializers.ModelSerializer):
    """
    检验汇报类型层级结构--third
    """
    inspectionReportType_child = InspectionReportTypeDefinitionSerialize_Fourth(many=True)  # 子类别信息
    class Meta:
        model = InspectionReportTypeDefinitionModel
        fields = ("id", "name", "code", "state", "inspectionReportType_child")

class InspectionReportTypeDefinitionSerialize_Second(serializers.ModelSerializer):
    """
    检验汇报类型层级结构--second
    """
    inspectionReportType_child = InspectionReportTypeDefinitionSerialize_Third(many=True)  # 子类别信息
    class Meta:
        model = InspectionReportTypeDefinitionModel
        fields = ("id", "name", "code", "state", "inspectionReportType_child")

class InspectionReportTypeDefinitionSerialize_First(serializers.ModelSerializer):
    """
    检验汇报类型层级结构--fitst
    """
    inspectionReportType_child = InspectionReportTypeDefinitionSerialize_Second(many=True) # 子类别信息
    class Meta:
        model = InspectionReportTypeDefinitionModel
        fields = ("id", "name", "code", "state","inspectionReportType_child")

# endregion

# region  品质看板定义  序列化器
class QualityBoardSerialize_Create(serializers.ModelSerializer):

    """
    品质看板定义--create
    """
    state= serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = QualityBoardModel
        fields = ("id", "name", "code","state", "image", "file","desc", "auditor","create_user"
                  )
    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('quality.add_qualityboardmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('quality.admin_qualityboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class  QualityBoardSerialize_List(serializers.ModelSerializer):

    """
    品质看板定义--list
    """
    image = QualityImageSerialize_List()
    class Meta:
        model = QualityBoardModel
        fields = ("id", "name", "code", "state","image","create_user","auditor","create_time","update_time")


class QualityBoardSerialize_Retrieve(serializers.ModelSerializer):

    """
    品质看板定义--retrieve
    """
    image = QualityImageSerialize_List()
    file =QualityFileSerialize_List(many=True)
    alter = QualityAlterRecordSerialize_List(many=True)

    class Meta:
        model = QualityBoardModel
        fields = "__all__"


class QualityBoardSerialize_Update(serializers.ModelSerializer):
    """
    品质看板定义--update
    """

    class Meta:
        model = QualityBoardModel
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
        if not auditor.has_perm('quality.admin_qualityboardmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class QualityBoardSerialize_Partial(serializers.ModelSerializer):
    """
    品质看板定义--partial
    """

    class Meta:
        model = QualityBoardModel
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
        obj = QualityBoardModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion