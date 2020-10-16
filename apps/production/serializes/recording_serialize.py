from rest_framework import serializers
from apps.production.serializes.basicinfor_serialize import  *
from apps.production.models.recording_model import *
from apps.process.models.basicinfor_model import *
from apps.plan.models.basicinfor_model import *
from commonFunction import *
from django.contrib.auth import get_user_model
from Mes import settings
User= get_user_model()

# region 考核信息定义 序列化器
class AssessmentRecordSerialize_Create(serializers.ModelSerializer):
    """
    考核信息定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AssessmentRecordModel
        fields = ("id", "name", "code", "state","type","personnel","level","dataTime",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "image", "file","desc", "auditor", "create_user"
                  )

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_assessmentrecordmodel'):  # 如果当前用户没有创建权限
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
        if not auditor.has_perm('production.admin_assessmentrecordmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        list = AssessmentTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 等级字段验证
    def validate_level(self, value):
        list = AssessmentLevelDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的等级不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的等级不在--'使用状态'")
        return value

class AssessmentRecordSerialize_List(serializers.ModelSerializer):
    """
    考核信息定义--list
    """
    type = AssessmentTypeDefinitionSerialize_List(required=False)
    personnel=PersonnelInforDefinitionSerialize_List()
    class Meta:
        model = AssessmentRecordModel
        fields = ("id", "name", "code", "state","type","personnel","dataTime", "auditor", "create_user","create_time","update_time"
                  )

class AssessmentRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    考核信息定义--retrieve
    """
    image =ProductionImageSerialize_List(many=True)
    file =ProductionFileSerialize_List(many=True)
    alter =ProductionAlterRecordSerialize_List(many=True)
    type = AssessmentTypeDefinitionSerialize_List(required=False)
    personnel=PersonnelInforDefinitionSerialize_List()
    level = AssessmentLevelDefinitionSerialize_List()

    class Meta:
        model = AssessmentRecordModel
        fields = "__all__"

class AssessmentRecordSerialize_Update(serializers.ModelSerializer):
    """
    考核信息定义--update
    """

    class Meta:
        model = AssessmentRecordModel
        fields = ("id", "name", "code", "type","personnel","level","dataTime",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5",
                  "image", "file","desc", "auditor"
                  )
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
        if not auditor.has_perm('production.admin_AssessmentRecordmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 类型字段验证
    def validate_type(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = AssessmentTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value

    # 等级字段验证
    def validate_level(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = AssessmentLevelDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的等级不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的等级不在--'使用状态'")
        return value

class AssessmentRecordSerialize_Partial(serializers.ModelSerializer):
    """
    考核信息定义--partial
    """

    class Meta:
        model = AssessmentRecordModel
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
             (self.instance.auditor != self.context['request'].user.username)):  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")):
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value):
        obj = AssessmentRecordModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value
# endregion
# region 产品生产日报子项定义 序列化器
class ProductDailyReportItemSerialize_Create(serializers.ModelSerializer):
    """
    产品生产日报子项定义--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductDailyReportItemModel
        fields = ("id", "handler","producttask_code","product_id", "all_sum", "ok_sum", "ng_sum",
                  "attribute1","attribute2","attribute3","attribute4","attribute5","image","file","desc","create_user")

    # 所有字段验证
    def validate(self, attrs):
        try:
            product = ProductInforDefinitionModel.objects.get(id=attrs["product_id"])  # 判断指定的产品是否存在
        except Exception as e:
            raise serializers.ValidationError("指定的产品不存在")
        if product.state != "使用中":
            raise serializers.ValidationError("指定的产品不在'使用中'状态")
        if 'producttask_code' in attrs.keys():
            if attrs['producttask_code'] is not '':
                try:
                    task = ProductTaskCreateModel.objects.get(code=attrs["producttask_code"])  # 判断指定的生产任务是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的生产任务不存在")
                attrs["producttask_name"] = task.name  # 获取生产任务名称
        attrs["productType_code"] = product.type.code  # 获取产品类型编码
        attrs["productType_name"] = product.type.name  # 获取产品类型名称
        attrs["product_code"] = product.code  # 获取产品编码
        attrs["product_name"] = product.name  # 获取产品名称
        return attrs



class ProductDailyReportItemSerialize_List(serializers.ModelSerializer):
    """
    产品生产日报子项定义--list
    """
    image = ProductionImageSerialize_List(many=True)
    file = ProductionFileSerialize_List(many=True)

    class Meta:
        model = ProductDailyReportItemModel
        fields = "__all__"


# endregion
# region 产品生产日报定义 序列化器
class ProductDailyReportSerialize_Create(serializers.ModelSerializer):
    """
    产品生产日报定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProductDailyReportModel
        fields = ("id", "name", "code", "state", "team", "child","attribute1", "attribute2","attribute3", "attribute4", "attribute5",
                  "image", "file","dataTime","desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_productdailyreportmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        attrs["workshop_code"] = attrs["team"].type.code  # 获取车间编码
        attrs["workshop_name"] = attrs["team"].type.name # 获取车间名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('production.admin_productdailyreportmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 班组字段验证
    def validate_team(self, value):
        list = TeamInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的班组不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的班组不在--'使用状态'")
        return value


class ProductDailyReportSerialize_List(serializers.ModelSerializer):
    """
    产品生产日报定义--list
    """
    team=TeamInforDefinitionSerialize_List(required=False)
    class Meta:
        model = ProductDailyReportModel
        fields = ("id", "name", "code","team","workshop_code","workshop_name", "state", "dataTime",
                  "auditor", "create_user","create_time","update_time")

class ProductDailyReportSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品生产日报定义--retrieve
    """
    image = ProductionImageSerialize_List(many=True)
    file = ProductionFileSerialize_List(many=True)
    alter = ProductionAlterRecordSerialize_List(many=True)
    team = TeamInforDefinitionSerialize_List(required=False)
    child =ProductDailyReportItemSerialize_List(many=True)

    class Meta:
        model = ProductDailyReportModel
        fields = "__all__"


class  ProductDailyReportSerialize_Update(serializers.ModelSerializer):
    """
    产品生产日报定义--update
    """

    class Meta:
        model = ProductDailyReportModel
        fields = ("id", "name", "code", "team", "child","attribute1", "attribute2","attribute3", "attribute4", "attribute5", "image",
                  "file","dataTime","desc", "auditor")

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
        if not auditor.has_perm('production.admin_productdailyreportmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 班组字段验证
    def validate_team(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = TeamInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的班组不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的班组不在--'使用状态'")
        return value

class ProductDailyReportSerialize_Partial(serializers.ModelSerializer):
    """
    产品生产日报定义--partial
    """

    class Meta:
        model = ProductDailyReportModel
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
        obj = ProductDailyReportModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion
# region 半成品生产日报子项定义 序列化器
class SemifinishedDailyReportItemSerialize_Create(serializers.ModelSerializer):
    """
    半成品生产日报子项定义--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedDailyReportItemModel
        fields = ("id", "handler","producttask_code", "semifinished_id", "all_sum", "ok_sum", "ng_sum",
                  "attribute1","attribute2","attribute3","attribute4","attribute5","image","file","desc","create_user")


    # 所有字段验证
    def validate(self, attrs):
        try:
            semifinished = SemifinishedInforDefinitionModel.objects.get(id=attrs["semifinished_id"])  # 判断指定的半成品是否存在
        except Exception as e:
            raise serializers.ValidationError("指定的半成品不存在")
        if semifinished.state != "使用中":
            raise serializers.ValidationError("指定的半成品不在'使用中'状态")
        if 'producttask_code' in attrs.keys():
            if attrs['producttask_code'] is not '':
                try:
                    task = ProductTaskCreateModel.objects.get(code=attrs["producttask_code"])  # 判断指定的生产任务是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的生产任务不存在")
                attrs["producttask_name"] = task.name  # 获取生产任务名称
        attrs["producttask_name"] = task.name  # 获取生产任务名称
        attrs["semifinished"] = semifinished.type.code  # 获取半成品类型编码
        attrs["semifinished"] = semifinished.type.name  # 获取半成品类型名称
        attrs["semifinished"] = semifinished.code  # 获取半成品编码
        attrs["semifinished"] = semifinished.name  # 获取半成品名称
        return attrs



class SemifinishedDailyReportItemSerialize_List(serializers.ModelSerializer):
    """
    半成品生产日报子项定义--list
    """
    image = ProductionImageSerialize_List(many=True)
    file = ProductionFileSerialize_List(many=True)

    class Meta:
        model = SemifinishedDailyReportItemModel
        fields = "__all__"


# endregion
# region 半成品生产日报定义 序列化器
class SemifinishedDailyReportSerialize_Create(serializers.ModelSerializer):
    """
    半成品生产日报定义--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SemifinishedDailyReportModel
        fields = ("id", "name", "code", "state", "team", "child","attribute1", "attribute2","attribute3", "attribute4", "attribute5",
                  "image", "file","dataTime","desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_semifinisheddailyreportmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER!=True:
            if attrs["create_user"].username == attrs["auditor"]:   # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        attrs["workshop_code"] = attrs["team"].type.code  # 获取车间编码
        attrs["workshop_name"] = attrs["team"].type.name  # 获取车间名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value):
        try:
            auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('production.admin_semifinisheddailyreportmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 班组字段验证
    def validate_team(self, value):
        list = TeamInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的班组不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的班组不在--'使用状态'")
        return value


class SemifinishedDailyReportSerialize_List(serializers.ModelSerializer):
    """
    半成品生产日报定义--list
    """
    team=TeamInforDefinitionSerialize_List(required=False)
    class Meta:
        model = SemifinishedDailyReportModel
        fields = ("id", "name", "code","team","workshop_code","workshop_name","state", "dataTime",
                  "auditor", "create_user","create_time","update_time"
                  )

class SemifinishedDailyReportSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品生产日报定义--retrieve
    """
    image = ProductionImageSerialize_List(many=True)
    file =  ProductionFileSerialize_List(many=True)
    alter = ProductionAlterRecordSerialize_List(many=True)
    team =  TeamInforDefinitionSerialize_List(required=False)
    child = SemifinishedDailyReportItemSerialize_List(many=True)

    class Meta:
        model = SemifinishedDailyReportModel
        fields = "__all__"


class SemifinishedDailyReportSerialize_Update(serializers.ModelSerializer):
    """
    半成品生产日报定义--update
    """

    class Meta:
        model = SemifinishedDailyReportModel
        fields = ("id", "name", "code", "team", "child","attribute1", "attribute2","attribute3", "attribute4", "attribute5",
                  "image", "file","dataTime","desc", "auditor")

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
        if not auditor.has_perm('production.admin_semifinisheddailyreportmodel'):
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value

    # 班组字段验证
    def validate_team(self, value):
        if self.instance.state != '新建':  # 如果不是新建状态 该字段不能更改
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        list = TeamInforDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的班组不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的班组不在--'使用状态'")
        return value

class SemifinishedDailyReportSerialize_Partial(serializers.ModelSerializer):
    """
    半成品生产日报定义--partial
    """

    class Meta:
        model = SemifinishedDailyReportModel
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
        obj = SemifinishedDailyReportModel.objects.get(id=self.instance.id).alter
        for data in value:
            obj.add(data.id)
        return value

# endregion
# region 产品过程数据定义 序列化器
class ProductDataSerialize_Create(serializers.ModelSerializer):
    """
    产品过程数据定义--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = ProductDataDefinitionModel
        fields = ("id","type","product_id","batch","sn","personnel","equipment","material","station","quality","dataTime",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5","attribute6", "attribute7", "attribute8", "attribute9", "attribute10",
                  "attribute11", "attribute12", "attribute13", "attribute14", "attribute15","attribute16", "attribute17", "attribute18", "attribute19", "attribute20",
                  "image", "file","desc", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_productdatadefinitionmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if 'product_id' in attrs.keys():
            if attrs['product_id'] is not '':
                try:
                    product = ProductInforDefinitionModel.objects.get(id=attrs["product_id"])  # 判断指定的产品是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的产品不存在")
                attrs["productType_code"] = product.type.code  # 获取产品类型编码
                attrs["productType_name"] = product.type.name  # 获取产品类型名称
                attrs["product_code"] = product.code  # 获取产品编码
                attrs["product_name"] = product.name  # 获取产品名称
        return attrs


    # 类型字段验证
    def validate_type(self, value):
        list = ProductDataTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class ProductDataSerialize_List(serializers.ModelSerializer):
    """
    产品过程数据定义--list
    """
    type = ProductDataTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = ProductDataDefinitionModel
        fields = ("id","type","productType_code","productType_name","product_name","product_id","product_code","batch","sn",
                  "personnel","equipment","material","station","quality","dataTime","desc", "create_user")

class ProductDataSerialize_Retrieve(serializers.ModelSerializer):
    """
    产品过程数据定义--retrieve
    """
    image =ProductionImageSerialize_List(many=True)
    file =ProductionFileSerialize_List(many=True)
    type = ProductDataTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = ProductDataDefinitionModel
        fields = "__all__"
# endregion
# region 半成品过程数据定义 序列化器
class SemifinishedDataSerialize_Create(serializers.ModelSerializer):
    """
    半成品过程数据定义--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = SemifinishedDataDefinitionModel
        fields = ("id","type","semifinished_id","batch","sn","personnel","equipment","material","station","quality","dataTime",
                  "attribute1", "attribute2", "attribute3", "attribute4","attribute5","attribute6", "attribute7", "attribute8", "attribute9", "attribute10",
                  "attribute11", "attribute12", "attribute13", "attribute14", "attribute15","attribute16", "attribute17", "attribute18", "attribute19", "attribute20",
                  "image", "file","desc", "create_user")

    # 所有字段验证
    def validate(self, attrs):
        if not attrs["create_user"].has_perm('production.add_semifinisheddatadefinitionmodel'):  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if 'semifinished_id' in attrs.keys():
            if attrs['semifinished_id'] is not '':
                try:
                    semifinished = SemifinishedInforDefinitionModel.objects.get(id=attrs["semifinished_id"])  # 判断指定的半成品是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的半成品不存在")
                attrs["semifinishedType_code"] = semifinished.type.code  # 获取半成品类型编码
                attrs["semifinishedType_name"] = semifinished.type.name  # 获取半成品类型名称
                attrs["semifinished_code"] = semifinished.code  # 获取半成品编码
                attrs["semifinished_name"] = semifinished.name  # 获取半成品名称
        return attrs


    # 类型字段验证
    def validate_type(self, value):
        list = SemifinishedDataTypeDefinitionModel.objects.get(id=value.id)
        if list is None:  # 判断 父类别是否存在
            raise serializers.ValidationError("指定的类型不存在")
        elif (list.state != "使用中"):  # 判断 父类别状态是否合适
            raise serializers.ValidationError("指定的类型不在--'使用状态'")
        return value


class SemifinishedDataSerialize_List(serializers.ModelSerializer):
    """
    半成品过程数据定义--list
    """
    type = SemifinishedDataTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = SemifinishedDataDefinitionModel
        fields = ("id","type","semifinishedType_code","semifinishedType_name","semifinished_name","semifinished_id","semifinished_code","batch","sn",
                  "personnel","equipment","material","station","quality","dataTime","desc", "create_user")

class SemifinishedDataSerialize_Retrieve(serializers.ModelSerializer):
    """
    半成品过程数据定义--retrieve
    """
    image =ProductionImageSerialize_List(many=True)
    file =ProductionFileSerialize_List(many=True)
    type = SemifinishedDataTypeDefinitionSerialize_List(required=False)
    class Meta:
        model = SemifinishedDataDefinitionModel
        fields = "__all__"
# endregion

