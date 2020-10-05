from rest_framework import serializers
from apps.quality.models.recording_model import *
from apps.quality.serializes.basicinfor_serialize import *
from commonFunction import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()

# region 检验汇报子项定义 序列化器
class ReportInforItemDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    检验汇报子项定义--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InspectionReportItemModel
        fields = ("id", "defect", "ok_sum", "ng_sum", "concession_sum", "image", "file","attribute1", "attribute2",
                  "attribute3", "attribute4","attribute5", "desc", "create_user")


class ReportInforItemDefinitionSerialize_List(serializers.ModelSerializer):
    """
    检验汇报子项定义--list
    """
    image = QualityImageSerialize_List(many=True)
    file = QualityFileSerialize_List(many=True)
    defect =DefectInforDefinitionSerialize_List()

    class Meta:
        model = InspectionReportItemModel
        fields = "__all__"


# endregion
# region 检验汇报定义 序列化器
class ReportInforDefinitionSerialize_Create(serializers.ModelSerializer):
    """
    检验汇报定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InspectionReportModel
        fields = ("id", "name", "code", "state", "type", "child","submit_sum","samples_sum","ok_sum","ng_sum","concession_sum","result","handler","dataTime",
                  "attribute1", "attribute2","attribute3", "attribute4", "attribute5", "image", "file","desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('quality.add_inspectionreportmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('quality.admin_inspectionreportmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = InspectionReportTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class ReportInforDefinitionSerialize_List(serializers.ModelSerializer):
    """
    检验汇报定义--list
    """
    type = InspectionReportTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = InspectionReportModel
        fields = ("id", "name", "code", "state", "type", "dataTime", "handler",
                  "result","auditor", "create_user","create_time","update_time")

class ReportInforDefinitionSerialize_Retrieve(serializers.ModelSerializer):
    """
    检验汇报定义--retrieve
    """
    image = QualityImageSerialize_List(many=True)
    file = QualityFileSerialize_List(many=True)
    alter = QualityAlterRecordSerialize_List(many=True)
    type = InspectionReportTypeDefinitionSerialize_List(required=False)
    child = ReportInforItemDefinitionSerialize_List(many=True)

    class Meta:
        model = InspectionReportModel
        fields = "__all__"


class ReportInforDefinitionSerialize_Update(serializers.ModelSerializer):
    """
    检验汇报定义--update
    """

    class Meta:
        model = InspectionReportModel
        fields = ("id", "name", "code", "type", "child","submit_sum","samples_sum","ok_sum","ng_sum","concession_sum","result","handler","dataTime",
                  "attribute1", "attribute2", "attribute3", "attribute4", "attribute5", "image", "file", "desc", "auditor")

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
        if not auditor.has_perm('quality.admin_inspectionreportmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = InspectionReportTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

class ReportInforDefinitionSerialize_Partial(serializers.ModelSerializer):
    """
    检验汇报定义--partial
    """

    class Meta:
        model = InspectionReportModel
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
        obj = InspectionReportModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion