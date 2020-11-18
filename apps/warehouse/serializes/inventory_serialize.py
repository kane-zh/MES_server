from rest_framework import serializers
from apps.warehouse.models.inventory_model import *
from apps.warehouse.serializes.basicinfor_serialize import *
from commonFunction import *
from django.contrib.auth import get_user_model
from apps.process.models.basicinfor_model import *
from apps.equipment.models.basicinfor_model import *
from apps.quality.models.basicinfor_model import *
from apps.quality.models.recording_model import *

from Mes import settings

User = get_user_model()


# region 库存明细定义  序列化器
class EquipmentStockDetailSerialize_List(serializers.ModelSerializer) :
    """
    设备库存明细--list
    """

    class Meta :
        model = EquipmentStockDetailModel
        fields = "__all__"


class PartsStockDetailSerialize_List(serializers.ModelSerializer) :
    """
    设备配件库存明细--list
    """

    class Meta :
        model = PartsStockDetailModel
        fields = "__all__"


class MaterialStockDetailSerialize_List(serializers.ModelSerializer) :
    """
    物料库存明细--list
    """

    class Meta :
        model = MaterialStockDetailModel
        fields = "__all__"


class ProductStockDetailSerialize_List(serializers.ModelSerializer) :
    """
    产品库存明细--list
    """

    class Meta :
        model = ProductStockDetailModel
        fields = "__all__"


class SemifinishedStockDetailSerialize_List(serializers.ModelSerializer) :
    """
    半成品库存明细--list
    """

    class Meta :
        model = SemifinishedStockDetailModel
        fields = "__all__"


# endregion


# region 库存信息定义  序列化器
class EquipmentStockInforSerialize_List(serializers.ModelSerializer) :
    """
    设备库存信息--list
    """

    class Meta :
        model = EquipmentStockInforModel
        fields = "__all__"


class PartsStockInforSerialize_List(serializers.ModelSerializer) :
    """
    设备配件库存信息--list
    """

    class Meta :
        model = PartsStockInforModel
        fields = "__all__"


class MaterialStockInforSerialize_List(serializers.ModelSerializer) :
    """
    物料库存信息--list
    """

    class Meta :
        model = MaterialStockInforModel
        fields = "__all__"


class ProductStockInforSerialize_List(serializers.ModelSerializer) :
    """
    产品库存信息--list
    """

    class Meta :
        model = ProductStockInforModel
        fields = "__all__"


class SemifinishedStockInforSerialize_List(serializers.ModelSerializer) :
    """
    半成品库存信息--list
    """

    class Meta :
        model = SemifinishedStockInforModel
        fields = "__all__"


# endregion

# region 设备管理  序列化器

class EquipmentManageSerialize_Create(serializers.ModelSerializer) :
    """
    设备管理--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = EquipmentManageModel
        fields = ("id", "name", "code", "state", "type", "position_id", "equipment_id", "handler", "sum", "dataTime",
                  "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user", "auditor"
                  )

    # 所有字段验证
    def validate(self, attrs) :
        if not attrs["create_user"].has_perm('warehouse.add_equipmentmanagemodel') :  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True :
            if attrs["create_user"].username == attrs["auditor"] :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            equipment = EquipmentAccountModel.objects.get(id=attrs["equipment_id"])  # 判断指定的设备是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的设备不存在")
        if equipment.state != "使用中" :
            raise serializers.ValidationError("指定的设备不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["equipmentType_code"] = equipment.type.code  # 获取设备类型编码
        attrs["equipmentType_name"] = equipment.type.name  # 获取设备类型名称
        attrs["equipment_code"] = equipment.code  # 获取设备编码
        attrs["equipment_name"] = equipment.name  # 获取设备名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_equipmentmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class EquipmentManageSerialize_List(serializers.ModelSerializer) :
    """
    设备管理--list
    """

    class Meta :
        model = EquipmentManageModel
        fields = ("id", "name", "code", "state", "type", "warehouse_name", "warehouse_code", "position_code", "position_name",
        "equipment_code", "equipment_name", "handler", "sum", "dataTime", "auditor", "create_user","create_time","update_time")


class EquipmentManageSerialize_Retrieve(serializers.ModelSerializer) :
    """
    设备管理--retrieve
    """
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta :
        model = EquipmentManageModel
        fields = "__all__"


class EquipmentManageSerialize_Update(serializers.ModelSerializer) :
    """
    设备管理--update
    """

    class Meta :
        model = EquipmentManageModel
        fields = (
        "id", "name", "code", "type", "position_id", "equipment_id", "handler", "sum", "dataTime", "attribute1",
        "attribute2",
        "attribute3", "attribute4", "attribute5", "desc", "auditor", "alter")

    # 所有字段验证
    def validate(self, attrs) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            equipment = EquipmentAccountModel.objects.get(id=attrs["equipment_id"])  # 判断指定的设备是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的设备不存在")
        if equipment.state != "使用中" :
            raise serializers.ValidationError("指定的设备不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["equipmentType_code"] = equipment.type.code  # 获取设备类型编码
        attrs["equipmentType_name"] = equipment.type.name  # 获取设备类型名称
        attrs["equipment_code"] = equipment.code  # 获取设备编码
        attrs["equipment_name"] = equipment.name  # 获取设备名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True :
            if self.instance.create_user == value :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_equipmentmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class EquipmentManageSerialize_Partial(serializers.ModelSerializer) :
    """
    设备管理--partial
    """

    class Meta :
        model = EquipmentManageModel
        fields = ("id", "state", "alter")

    # 入库操作条件判断
    def storage(self, state) :
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if position.state != "闲置" :  # 如果指定的仓位不处于‘空闲状态’
                raise serializers.ValidationError("当前仓位不在‘空闲状态’")
            if self.instance.sum > position.maximum :  # 如果操作数量超出了仓位最大容量
                raise serializers.ValidationError("操作数量超出了仓位的最大容量’")
            position.state = "使用中"  # 占用当前仓位(将状态置为‘使用中状态’)
            position.save()
        if state == "新建" :  # 驳回情况下
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()
        if state == "完成" :  # 通过审核情况下
            EquipmentStockDetailModel.objects.create(  # 新建一条库存记录
                state="使用中",
                warehouse_code=self.instance.warehouse_code,
                warehouse_name=self.instance.warehouse_name,
                position_id=self.instance.position_id,
                position_code=self.instance.position_code,
                position_name=self.instance.position_name,
                equipmentType_code=self.instance.equipmentType_code,
                equipmentType_name=self.instance.equipmentType_name,
                equipment_id=self.instance.equipment_id,
                equipment_code=self.instance.equipment_code,
                equipment_name=self.instance.equipment_name,
                sum=self.instance.sum,
                attribute1=self.instance.attribute1,
                attribute2=self.instance.attribute2,
                attribute3=self.instance.attribute3,
                attribute4=self.instance.attribute4,
                attribute5=self.instance.attribute5)
            condtions1 = {'equipment_id__iexact' : self.instance.equipment_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          }
            try :
                equipmentStockInfor = EquipmentStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
                equipmentStockInfor.sum += self.instance.sum  # 更新库存数量
                equipmentStockInfor.save()
            except Exception as e :
                EquipmentStockInforModel.objects.create(  # 新建一条库存记录
                    warehouse_code=self.instance.warehouse_code,
                    warehouse_name=self.instance.warehouse_name,
                    equipmentType_code=self.instance.equipmentType_code,
                    equipmentType_name=self.instance.equipmentType_name,
                    equipment_id=self.instance.equipment_id,
                    equipment_code=self.instance.equipment_code,
                    equipment_name=self.instance.equipment_name,
                    sum=self.instance.sum,
                    attribute1=self.instance.attribute1,
                    attribute2=self.instance.attribute2,
                    attribute3=self.instance.attribute3,
                    attribute4=self.instance.attribute4,
                    attribute5=self.instance.attribute5)
        if state == "作废" and self.instance.state == "审核中" :  # 如果审核过程中报废信息
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()

    # 增加操作  条件判断
    def increase(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'equipment_id__iexact' : self.instance.equipment_id,
                     'position_id__iexact' : self.instance.position_id,
                     }
        if state == "作废" :
            return
        try :
            equipmentStockDetail = EquipmentStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if (self.instance.sum + equipmentStockDetail.sum) > position.maximum :  # 如果操作数量+库存数量 超出库存数量
                raise serializers.ValidationError("当前增加数量加库存数量超出仓位最大容量")
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'equipment_id__iexact' : self.instance.equipment_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          }
            try :
                equipmentStockInfor = EquipmentStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            equipmentStockInfor.sum += self.instance.sum  # 更新库存数量
            equipmentStockInfor.save()
            equipmentStockDetail.sum += self.instance.sum  # 更新库存数量
            equipmentStockDetail.save()

    # 出库操作 条件判断
    def outbound(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'equipment_id__iexact' : self.instance.equipment_id,
                     'position_id__iexact' : self.instance.position_id,
                     }
        if state == "作废" :
            return
        try :
            equipmentStockDetail = EquipmentStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行出库操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" or state == "完成":  # 提交情况下
           if self.instance.sum > equipmentStockDetail.sum :  # 如果操作数量超出库存数量
               raise serializers.ValidationError("当前出库数量超出库存数量")
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'equipment_id__iexact' : self.instance.equipment_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          }
            try :
                equipmentStockInfor = EquipmentStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            equipmentStockInfor.sum -= self.instance.sum  # 更新库存数量
            equipmentStockInfor.save()
            equipmentStockDetail.sum -= self.instance.sum  # 更新库存数量
            equipmentStockDetail.save()
            if (equipmentStockDetail.sum <= 0) :
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                equipmentStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                equipmentStockDetail.save()

    # 盘点操作 条件判断
    def inventory(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'equipment_id__iexact' : self.instance.equipment_id,
                     'position_id__iexact' : self.instance.position_id,
                     }
        if state == "作废" :
            return
        try :
            equipmentStockDetail = EquipmentStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'equipment_id__iexact' : self.instance.equipment_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          }
            try :
                equipmentStockInfor = EquipmentStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            equipmentStockInfor.sum += self.instance.sum  # 更新库存数量
            equipmentStockInfor.save()
            equipmentStockDetail.sum += self.instance.sum  # 更新库存数量
            equipmentStockDetail.save()
            if (equipmentStockDetail.sum <= 0) :
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                equipmentStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                equipmentStockDetail.save()

    # 所有字段验证
    def validate(self, attrs) :
        try :
            del attrs['alter']  # 删除alter字段
        except Exception :
            pass
        if self.instance.type == "增加操作" :
            self.increase(attrs['state'])
        elif self.instance.type == "入库操作" or self.instance.type == "退库操作" :
            self.storage(attrs['state'])
        elif self.instance.type == "出库操作" :
            self.outbound(attrs['state'])
        elif self.instance.type == "盘点操作" :
            self.inventory(attrs['state'])
        return attrs

    # 状态字段验证
    def validate_state(self, value) :
        if ((self.instance.create_user == self.context['request'].user.username) and \
                (self.instance.auditor != self.context['request'].user.username)) :  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")) :
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "新建" and \
                (value == "审核中" or value == "作废")) :
            return value
        if (self.instance.state == "审核中" and \
                (value == "完成" or value == "新建" or value == "作废")) :
            return value
        if (self.instance.state == "完成" and \
                (value == "作废")) :
            return value
        raise serializers.ValidationError("不能从" + self.instance.state + "更新到" + value)
        return value

    # 审核记录字段验证
    def validate_alter(self, value) :
        obj = EquipmentManageModel.objects.get(id=self.instance.id).alter
        for data in value :
            obj.add(data.id)
        return value


# endregion

# region 设备配件管理  序列化器

class PartsManageSerialize_Create(serializers.ModelSerializer) :
    """
    设备配件管理--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = PartsManageModel
        fields = (
        "id", "name", "code", "state", "type", "position_id", "parts_id", "handler", "sum", "dataTime", "attribute1",
        "attribute2",
        "attribute3", "attribute4", "attribute5", "desc", "create_user", "auditor"
        )

    # 所有字段验证
    def validate(self, attrs) :
        if not attrs["create_user"].has_perm('warehouse.add_partsmanagemodel') :  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True :
            if attrs["create_user"].username == attrs["auditor"] :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            parts = PartsInforDefinitionModel.objects.get(id=attrs["parts_id"])  # 判断指定的设备配件是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的设备配件不存在")
        if parts.state != "使用中" :
            raise serializers.ValidationError("指定的设备配件不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["partsType_code"] = parts.type.code  # 获取设备配件类型编码
        attrs["partsType_name"] = parts.type.name  # 获取设备配件类型名称
        attrs["parts_code"] = parts.code  # 获取设备配件编码
        attrs["parts_name"] = parts.name  # 获取设备配件名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_partsmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class PartsManageSerialize_List(serializers.ModelSerializer) :
    """
    设备配件管理--list
    """

    class Meta :
        model = PartsManageModel
        fields = ("id", "name", "code", "state", "type", "warehouse_name", "warehouse_code", "position_code", "position_name",
        "parts_code", "parts_name", "handler", "sum", "dataTime", "auditor", "create_user","create_time","update_time")


class PartsManageSerialize_Retrieve(serializers.ModelSerializer) :
    """
    设备配件管理--retrieve
    """
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta :
        model = PartsManageModel
        fields = "__all__"


class PartsManageSerialize_Update(serializers.ModelSerializer) :
    """
    设备配件管理--update
    """

    class Meta :
        model = PartsManageModel
        fields = ("id", "name", "code", "type", "position_id", "parts_id", "handler", "sum", "dataTime", "attribute1",
                  "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor", "alter")

    # 所有字段验证
    def validate(self, attrs) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            parts = PartsInforDefinitionModel.objects.get(id=attrs["parts_id"])  # 判断指定的设备配件是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的设备配件不存在")
        if parts.state != "使用中" :
            raise serializers.ValidationError("指定的设备配件不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["partsType_code"] = parts.type.code  # 获取设备配件类型编码
        attrs["partsType_name"] = parts.type.name  # 获取设备配件类型名称
        attrs["parts_code"] = parts.code  # 获取设备配件编码
        attrs["parts_name"] = parts.name  # 获取设备配件名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True :
            if self.instance.create_user == value :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_partsmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class PartsManageSerialize_Partial(serializers.ModelSerializer) :
    """
    设备配件管理--partial
    """

    class Meta :
        model = PartsManageModel
        fields = ("id", "state", "alter")

    # 入库操作条件判断
    def storage(self, state) :
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if position.state != "闲置" :  # 如果指定的仓位不处于‘空闲状态’
                raise serializers.ValidationError("当前仓位不在‘空闲状态’")
            if self.instance.sum > position.maximum :  # 如果操作数量超出了仓位最大容量
                raise serializers.ValidationError("操作数量超出了仓位的最大容量’")
            position.state = "使用中"  # 占用当前仓位(将状态置为‘使用中状态’)
            position.save()
        if state == "新建" :  # 驳回情况下
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()
        if state == "完成" :  # 通过审核情况下
            PartsStockDetailModel.objects.create(  # 新建一条库存记录
                state="使用中",
                warehouse_code=self.instance.warehouse_code,
                warehouse_name=self.instance.warehouse_name,
                position_id=self.instance.position_id,
                position_code=self.instance.position_code,
                position_name=self.instance.position_name,
                partsType_code=self.instance.partsType_code,
                partsType_name=self.instance.partsType_name,
                parts_id=self.instance.parts_id,
                parts_code=self.instance.parts_code,
                parts_name=self.instance.parts_name,
                sum=self.instance.sum,
                attribute1=self.instance.attribute1,
                attribute2=self.instance.attribute2,
                attribute3=self.instance.attribute3,
                attribute4=self.instance.attribute4,
                attribute5=self.instance.attribute5)
            condtions1 = {'parts_id__iexact' : self.instance.parts_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          }
            try :
                partsStockInfor = PartsStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
                partsStockInfor.sum += self.instance.sum  # 更新库存数量
                partsStockInfor.save()
            except Exception as e :
                PartsStockInforModel.objects.create(  # 新建一条库存记录
                    warehouse_code=self.instance.warehouse_code,
                    warehouse_name=self.instance.warehouse_name,
                    partsType_code=self.instance.partsType_code,
                    partsType_name=self.instance.partsType_name,
                    parts_id=self.instance.parts_id,
                    parts_code=self.instance.parts_code,
                    parts_name=self.instance.parts_name,
                    sum=self.instance.sum,
                    attribute1=self.instance.attribute1,
                    attribute2=self.instance.attribute2,
                    attribute3=self.instance.attribute3,
                    attribute4=self.instance.attribute4,
                    attribute5=self.instance.attribute5)
        if state == "作废" and self.instance.state == "审核中" :  # 如果审核过程中报废信息
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()

    # 增加操作  条件判断
    def increase(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'parts_id__iexact' : self.instance.parts_id,
                     'position_id__iexact' : self.instance.position_id,
                     }
        if state == "作废" :
            return
        try :
            partsStockDetail = PartsStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if (self.instance.sum + partsStockDetail.sum) > position.maximum :  # 如果操作数量+库存数量 超出库存数量
                raise serializers.ValidationError("当前增加数量加库存数量超出仓位最大容量")
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'parts_id__iexact' : self.instance.parts_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          }
            try :
                partsStockInfor = PartsStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            partsStockInfor.sum += self.instance.sum  # 更新库存数量
            partsStockInfor.save()
            partsStockDetail.sum += self.instance.sum  # 更新库存数量
            partsStockDetail.save()

    # 出库操作 条件判断
    def outbound(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'parts_id__iexact' : self.instance.parts_id,
                     'position_id__iexact' : self.instance.position_id,
                     }
        if state == "作废" :
            return
        try :
            partsStockDetail = PartsStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行出库操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" or state == "完成":  # 提交情况下
            if self.instance.sum > partsStockDetail.sum :  # 如果操作数量超出库存数量
                raise serializers.ValidationError("当前出库数量超出库存数量")
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'parts_id__iexact' : self.instance.parts_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          }
            try :
                partsStockInfor = PartsStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            partsStockInfor.sum -= self.instance.sum  # 更新库存数量
            partsStockInfor.save()
            partsStockDetail.sum -= self.instance.sum  # 更新库存数量
            partsStockDetail.save()
            if (partsStockDetail.sum <= 0) :
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                partsStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                partsStockDetail.save()

    # 盘点操作 条件判断
    def inventory(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'parts_id__iexact' : self.instance.parts_id,
                     'position_id__iexact' : self.instance.position_id,
                     }
        if state == "作废" :
            return
        try :
            partsStockDetail = PartsStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'parts_id__iexact' : self.instance.parts_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          }
            try :
                partsStockInfor = PartsStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            partsStockInfor.sum += self.instance.sum  # 更新库存数量
            partsStockInfor.save()
            partsStockDetail.sum += self.instance.sum  # 更新库存数量
            partsStockDetail.save()
            if (partsStockDetail.sum <= 0) :
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                partsStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                partsStockDetail.save()

    # 所有字段验证
    def validate(self, attrs) :
        try :
            del attrs['alter']  # 删除alter字段
        except Exception :
            pass
        if self.instance.type == "增加操作" :
            self.increase(attrs['state'])
        elif self.instance.type == "入库操作" or self.instance.type == "退库操作" :
            self.storage(attrs['state'])
        elif self.instance.type == "出库操作" :
            self.outbound(attrs['state'])
        elif self.instance.type == "盘点操作" :
            self.inventory(attrs['state'])
        return attrs

    # 状态字段验证
    def validate_state(self, value) :
        if ((self.instance.create_user == self.context['request'].user.username) and \
                (self.instance.auditor != self.context['request'].user.username)) :  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")) :
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "新建" and \
                (value == "审核中" or value == "作废")) :
            return value
        if (self.instance.state == "审核中" and \
                (value == "完成" or value == "新建" or value == "作废")) :
            return value
        if (self.instance.state == "完成" and \
                (value == "作废")) :
            return value
        raise serializers.ValidationError("不能从" + self.instance.state + "更新到" + value)
        return value

    # 审核记录字段验证
    def validate_alter(self, value) :
        obj = PartsManageModel.objects.get(id=self.instance.id).alter
        for data in value :
            obj.add(data.id)
        return value


# endregion

# region 物料管理  序列化器

class MaterialManageSerialize_Create(serializers.ModelSerializer) :
    """
    物料管理--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = MaterialManageModel
        fields = ("id", "name", "code", "state", "type", "position_id", "material_id","inspectionReport_id", "handler", "batch",
                  "sum", "dataTime", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user", "auditor"
                  )
    # 所有字段验证
    def validate(self, attrs) :
        if not attrs["create_user"].has_perm('warehouse.add_materialmanagemodel') :  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True :
            if attrs["create_user"].username == attrs["auditor"] :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        if position.state != "闲置":
            raise serializers.ValidationError("指定的仓位不在'闲置'状态")
        try :
            material = MaterialInforDefinitionModel.objects.get(id=attrs["material_id"])  # 判断指定的物料是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的物料不存在")
        if material.state != "使用中" :
            raise serializers.ValidationError("指定的物料不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["materialType_code"] = material.type.code  # 获取物料类型编码
        attrs["materialType_name"] = material.type.name  # 获取物料类型名称
        attrs["material_code"] = material.code  # 获取物料编码
        attrs["material_name"] = material.name  # 获取物料名称
        if 'inspectionReport_id' in attrs.keys():
            if attrs['inspectionReport_id'] is not '':
                try:
                    report = InspectionReportModel.objects.get(id=attrs["inspectionReport_id"])  # 判断指定的质检报告是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的质检报告不存在")
                attrs["inspectionReportType_code"] = report.type.code  # 获取质检报告类型编码
                attrs["inspectionReportType_name"] = report.type.name  # 获取质检报告类型名称
                attrs["inspectionReport_code"] = report.code  # 获取质检报告编码
                attrs["inspectionReport_name"] = report.name  # 获取质检报告名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_materialmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class MaterialManageSerialize_List(serializers.ModelSerializer) :
    """
    物料管理--list
    """

    class Meta :
        model = MaterialManageModel
        fields = ("id", "name", "code", "state", "type", "warehouse_name", "warehouse_code", "position_code", "position_name",
        "material_code", "material_name", "handler", "batch", "sum", "dataTime", "auditor", "create_user","create_time","update_time")


class MaterialManageSerialize_Retrieve(serializers.ModelSerializer) :
    """
    物料管理--retrieve
    """
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta :
        model = MaterialManageModel
        fields = "__all__"


class MaterialManageSerialize_Update(serializers.ModelSerializer) :
    """
    物料管理--update
    """

    class Meta :
        model = MaterialManageModel
        fields = ("id", "name", "code", "type", "position_id", "material_id","inspectionReport_id", "handler", "batch",
                  "sum", "dataTime", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor", "alter")

    # 所有字段验证
    def validate(self, attrs) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            material = MaterialInforDefinitionModel.objects.get(id=attrs["material_id"])  # 判断指定的物料是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的物料不存在")
        if material.state != "使用中" :
            raise serializers.ValidationError("指定的物料不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["materialType_code"] = material.type.code  # 获取物料类型编码
        attrs["materialType_name"] = material.type.name  # 获取物料类型名称
        attrs["material_code"] = material.code  # 获取物料编码
        attrs["material_name"] = material.name  # 获取物料名称
        if 'inspectionReport_id' in attrs.keys():
            if attrs['inspectionReport_id'] is not '':
                try:
                    report = InspectionReportModel.objects.get(id=attrs["inspectionReport_id"])  # 判断指定的质检报告是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的质检报告不存在")
                attrs["inspectionReportType_code"] = report.type.code  # 获取质检报告类型编码
                attrs["inspectionReportType_name"] = report.type.name  # 获取质检报告类型名称
                attrs["inspectionReport_code"] = report.code  # 获取质检报告编码
                attrs["inspectionReport_name"] = report.name  # 获取质检报告名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True :
            if self.instance.create_user == value :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_materialmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class MaterialManageSerialize_Partial(serializers.ModelSerializer) :
    """
    物料管理--partial
    """

    class Meta :
        model = MaterialManageModel
        fields = ("id", "state", "alter")

    # 入库操作条件判断
    def storage(self, state) :
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if position.state != "闲置" :  # 如果指定的仓位不处于‘空闲状态’
                raise serializers.ValidationError("当前仓位不在‘空闲状态’")
            if self.instance.sum > position.maximum :  # 如果操作数量超出了仓位最大容量
                raise serializers.ValidationError("操作数量超出了仓位的最大容量’")
            position.state = "使用中"  # 占用当前仓位(将状态置为‘使用中状态’)
            position.save()
        if state == "新建" :  # 驳回情况下
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()
        if state == "完成" :  # 通过审核情况下
            MaterialStockDetailModel.objects.create(  # 新建一条库存记录
                state="使用中",
                warehouse_code=self.instance.warehouse_code,
                warehouse_name=self.instance.warehouse_name,
                position_id=self.instance.position_id,
                position_code=self.instance.position_code,
                position_name=self.instance.position_name,
                materialType_code=self.instance.materialType_code,
                materialType_name=self.instance.materialType_name,
                material_id=self.instance.material_id,
                material_code=self.instance.material_code,
                material_name=self.instance.material_name,
                batch=self.instance.batch,
                sum=self.instance.sum,
                attribute1=self.instance.attribute1,
                attribute2=self.instance.attribute2,
                attribute3=self.instance.attribute3,
                attribute4=self.instance.attribute4,
                attribute5=self.instance.attribute5)
            condtions1 = {'material_id__iexact' : self.instance.material_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                materialStockInfor = MaterialStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
                materialStockInfor.sum += self.instance.sum  # 更新库存数量
                materialStockInfor.save()
            except Exception as e :
                MaterialStockInforModel.objects.create(  # 新建一条库存记录
                    warehouse_code=self.instance.warehouse_code,
                    warehouse_name=self.instance.warehouse_name,
                    materialType_code=self.instance.materialType_code,
                    materialType_name=self.instance.materialType_name,
                    material_id=self.instance.material_id,
                    material_code=self.instance.material_code,
                    material_name=self.instance.material_name,
                    batch=self.instance.batch,
                    sum=self.instance.sum,
                    attribute1=self.instance.attribute1,
                    attribute2=self.instance.attribute2,
                    attribute3=self.instance.attribute3,
                    attribute4=self.instance.attribute4,
                    attribute5=self.instance.attribute5)
        if state == "作废" and self.instance.state == "审核中" :  # 如果审核过程中报废信息
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()

    # 增加操作  条件判断
    def increase(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'material_id__iexact' : self.instance.material_id,
                     'position_id__iexact' : self.instance.position_id,
                     'batch__iexact' : self.instance.batch
                     }
        if state == "作废" :
            return
        try :
            materialStockDetail = MaterialStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if (self.instance.sum + materialStockDetail.sum) > position.maximum :  # 如果操作数量+库存数量 超出库存数量
                raise serializers.ValidationError("当前增加数量加库存数量超出仓位最大容量")
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'material_id__iexact' : self.instance.material_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                materialStockInfor = MaterialStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            materialStockInfor.sum += self.instance.sum  # 更新库存数量
            materialStockInfor.save()
            materialStockDetail.sum += self.instance.sum  # 更新库存数量
            materialStockDetail.save()

    # # 出库操作 条件判断
    # def outbound(self, state) :
    #     condtions = {'state__iexact' : "使用中",
    #                  'material_id__iexact' : self.instance.material_id,
    #                  'position_id__iexact' : self.instance.position_id,
    #                  'batch__iexact' : self.instance.batch
    #                  }
    #     if state == "作废" :
    #         return
    #     try :
    #         materialStockDetail = MaterialStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
    #     except Exception as e :
    #         raise serializers.ValidationError("当前库存明细不存在,无法进行出库操作")
    #     position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
    #     if state == "审核中" or state == "完成":  # 提交情况下
    #         if self.instance.sum > materialStockDetail.sum :  # 如果操作数量超出库存数量
    #             raise serializers.ValidationError("当前出库数量超出库存数量")
    #     if state == "完成" :  # 通过审核情况下
    #         condtions1 = {'material_id__iexact' : self.instance.material_id,
    #                       'warehouse_code__iexact' : self.instance.warehouse_code,
    #                       'batch__iexact' : self.instance.batch
    #                       }
    #         try :
    #             materialStockInfor = MaterialStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
    #         except Exception as e :
    #             raise serializers.ValidationError("当前库存信息与库存明细不符合")
    #         materialStockInfor.sum -= self.instance.sum  # 更新库存数量
    #         materialStockInfor.save()
    #         materialStockDetail.sum -= self.instance.sum  # 更新库存数量
    #         materialStockDetail.save()
    #         if (materialStockDetail.sum <= 0) :
    #             position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
    #             position.save()
    #             materialStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
    #             materialStockDetail.save()
    def outbound(self, state):
        condtions = {'state__iexact': "使用中",
                     'material_id__iexact': self.instance.material_id,
                     'position_id__iexact': self.instance.position_id,
                     'batch__iexact': self.instance.batch
                     }
        try:
            materialStockDetail = MaterialStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e:
            raise serializers.ValidationError("当前库存明细不存在,无法进行出库操作")
        condtions1 = {'material_id__iexact': self.instance.material_id,
                      'warehouse_code__iexact': self.instance.warehouse_code,
                      'batch__iexact': self.instance.batch
                      }
        try:
            materialStockInfor = MaterialStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
        except Exception as e:
            raise serializers.ValidationError("当前库存信息与库存明细不符合")
        if (self.instance.state == "新建" and state == "作废"):
            return
        if (self.instance.state == "新建" and state == "审核中"):  # 提交情况下
            if self.instance.sum > materialStockDetail.sum:  # 如果操作数量超出库存数量
                raise serializers.ValidationError("当前出库数量超出库存数量")
            materialStockInfor.sum -= self.instance.sum  # 更新库存数量
            materialStockInfor.save()
            materialStockDetail.sum -= self.instance.sum  # 更新库存数量
            materialStockDetail.save()
        if (self.instance.state == "审核中" and state == "完成"):  # 通过审核情况下
            position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
            if (materialStockDetail.sum <= 0):
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                materialStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                materialStockDetail.save()
        if (self.instance.state == "审核中" and state == "新建"):  # 驳回情况下
            materialStockInfor.sum += self.instance.sum  # 更新库存数量
            materialStockInfor.save()
            materialStockDetail.sum += self.instance.sum  # 更新库存数量
            materialStockDetail.save()
        if (self.instance.state == "审核中" and state == "作废"):  # 审核作废情况下
            materialStockInfor.sum += self.instance.sum  # 更新库存数量
            materialStockInfor.save()
            materialStockDetail.sum += self.instance.sum  # 更新库存数量
            materialStockDetail.save()
    # 盘点操作 条件判断
    def inventory(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'material_id__iexact' : self.instance.material_id,
                     'position_id__iexact' : self.instance.position_id,
                     'batch__iexact' : self.instance.batch
                     }
        if state == "作废" :
            return
        try :
            materialStockDetail = MaterialStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'material_id__iexact' : self.instance.material_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                materialStockInfor = MaterialStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            materialStockInfor.sum += self.instance.sum  # 更新库存数量
            materialStockInfor.save()
            materialStockDetail.sum += self.instance.sum  # 更新库存数量
            materialStockDetail.save()
            if (materialStockDetail.sum <= 0) :
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                materialStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                materialStockDetail.save()

    # 所有字段验证
    def validate(self, attrs) :
        try :
            del attrs['alter']  # 删除alter字段
        except Exception :
            pass
        if self.instance.type == "增加操作" :
            self.increase(attrs['state'])
        elif self.instance.type == "入库操作" or self.instance.type == "退库操作" :
            self.storage(attrs['state'])
        elif self.instance.type == "出库操作" :
            self.outbound(attrs['state'])
        elif self.instance.type == "盘点操作" :
            self.inventory(attrs['state'])
        return attrs

    # 状态字段验证
    def validate_state(self, value) :
        if ((self.instance.create_user == self.context['request'].user.username) and \
                (self.instance.auditor != self.context['request'].user.username)) :  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")) :
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "新建" and \
                (value == "审核中" or value == "作废")) :
            return value
        if (self.instance.state == "审核中" and \
                (value == "完成" or value == "新建" or value == "作废")) :
            return value
        if (self.instance.state == "完成" and \
                (value == "作废")) :
            return value
        raise serializers.ValidationError("不能从" + self.instance.state + "更新到" + value)
        return value

    # 审核记录字段验证
    def validate_alter(self, value) :
        obj = MaterialManageModel.objects.get(id=self.instance.id).alter
        for data in value :
            obj.add(data.id)
        return value


# endregion

# region 半成品管理  序列化器

class SemifinishedManageSerialize_Create(serializers.ModelSerializer) :
    """
    半成品管理--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = SemifinishedManageModel
        fields = ("id", "name", "code", "state", "type", "position_id", "semifinished_id", "inspectionReport_id","handler", "batch",
                  "sum", "dataTime", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user", "auditor"
                  )

    # 所有字段验证
    def validate(self, attrs) :
        if not attrs["create_user"].has_perm('warehouse.add_semifinishedmanagemodel') :  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True :
            if attrs["create_user"].username == attrs["auditor"] :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            semifinished = SemifinishedInforDefinitionModel.objects.get(id=attrs["semifinished_id"])  # 判断指定的物料是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的半成品不存在")
        if semifinished.state != "使用中" :
            raise serializers.ValidationError("指定的半成品不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["semifinishedType_code"] = semifinished.type.code  # 获取半成品类型编码
        attrs["semifinishedType_name"] = semifinished.type.name  # 获取半成品类型名称
        attrs["semifinished_code"] = semifinished.code  # 获取半成品编码
        attrs["semifinished_name"] = semifinished.name  # 获取半成品名称
        if 'inspectionReport_id' in attrs.keys():
            if attrs['inspectionReport_id'] is not '':
                try:
                    report = InspectionReportModel.objects.get(id=attrs["inspectionReport_id"])  # 判断指定的质检报告是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的质检报告不存在")
                attrs["inspectionReportType_code"] = report.type.code  # 获取质检报告类型编码
                attrs["inspectionReportType_name"] = report.type.name  # 获取质检报告类型名称
                attrs["inspectionReport_code"] = report.code  # 获取质检报告编码
                attrs["inspectionReport_name"] = report.name  # 获取质检报告名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_semifinishedmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class SemifinishedManageSerialize_List(serializers.ModelSerializer) :
    """
    半成品管理--list
    """

    class Meta :
        model = SemifinishedManageModel
        fields = ( "id", "name", "code", "state", "type", "warehouse_name", "warehouse_code", "position_code", "position_name",
        "semifinished_code", "semifinished_name", "handler", "batch", "sum", "dataTime", "auditor", "create_user","create_time","update_time")


class SemifinishedManageSerialize_Retrieve(serializers.ModelSerializer) :
    """
    半成品管理--retrieve
    """
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta :
        model = SemifinishedManageModel
        fields = "__all__"


class SemifinishedManageSerialize_Update(serializers.ModelSerializer) :
    """
    半成品管理--update
    """

    class Meta :
        model = SemifinishedManageModel
        fields = ("id", "name", "code", "type", "position_id", "semifinished_id","inspectionReport_id", "handler", "batch",
                  "sum", "dataTime", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor", "alter")

    # 所有字段验证
    def validate(self, attrs) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            semifinished = SemifinishedInforDefinitionModel.objects.get(id=attrs["semifinished_id"])  # 判断指定的半成品是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的半成品不存在")
        if semifinished.state != "使用中" :
            raise serializers.ValidationError("指定的半成品不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["semifinishedType_code"] = semifinished.type.code  # 获取半成品类型编码
        attrs["semifinishedType_name"] = semifinished.type.name  # 获取半成品类型名称
        attrs["semifinished_code"] = semifinished.code  # 获取半成品编码
        attrs["semifinished_name"] = semifinished.name  # 获取半成品名称
        if 'inspectionReport_id' in attrs.keys():
            if attrs['inspectionReport_id'] is not '':
                try:
                    report = InspectionReportModel.objects.get(id=attrs["inspectionReport_id"])  # 判断指定的质检报告是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的质检报告不存在")
                attrs["inspectionReportType_code"] = report.type.code  # 获取质检报告类型编码
                attrs["inspectionReportType_name"] = report.type.name  # 获取质检报告类型名称
                attrs["inspectionReport_code"] = report.code  # 获取质检报告编码
                attrs["inspectionReport_name"] = report.name  # 获取质检报告名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True :
            if self.instance.create_user == value :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_semifinishedmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class SemifinishedManageSerialize_Partial(serializers.ModelSerializer) :
    """
    半成品管理--partial
    """

    class Meta :
        model = SemifinishedManageModel
        fields = ("id", "state", "alter")

    # 入库操作条件判断
    def storage(self, state) :
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if position.state != "闲置" :  # 如果指定的仓位不处于‘空闲状态’
                raise serializers.ValidationError("当前仓位不在‘空闲状态’")
            if self.instance.sum > position.maximum :  # 如果操作数量超出了仓位最大容量
                raise serializers.ValidationError("操作数量超出了仓位的最大容量’")
            position.state = "使用中"  # 占用当前仓位(将状态置为‘使用中状态’)
            position.save()
        if state == "新建" :  # 驳回情况下
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()
        if state == "完成" :  # 通过审核情况下
            SemifinishedStockDetailModel.objects.create(  # 新建一条库存记录
                state="使用中",
                warehouse_code=self.instance.warehouse_code,
                warehouse_name=self.instance.warehouse_name,
                position_id=self.instance.position_id,
                position_code=self.instance.position_code,
                position_name=self.instance.position_name,
                semifinishedType_code=self.instance.semifinishedType_code,
                semifinishedType_name=self.instance.semifinishedType_name,
                semifinished_id=self.instance.semifinished_id,
                semifinished_code=self.instance.semifinished_code,
                semifinished_name=self.instance.semifinished_name,
                batch=self.instance.batch,
                sum=self.instance.sum,
                attribute1=self.instance.attribute1,
                attribute2=self.instance.attribute2,
                attribute3=self.instance.attribute3,
                attribute4=self.instance.attribute4,
                attribute5=self.instance.attribute5
            )
            condtions1 = {'semifinished_id__iexact' : self.instance.semifinished_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                semifinishedStockInfor = SemifinishedStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
                semifinishedStockInfor.sum += self.instance.sum  # 更新库存数量
                semifinishedStockInfor.save()
            except Exception as e :
                SemifinishedStockInforModel.objects.create(  # 新建一条库存记录
                    warehouse_code=self.instance.warehouse_code,
                    warehouse_name=self.instance.warehouse_name,
                    semifinishedType_code=self.instance.semifinishedType_code,
                    semifinishedType_name=self.instance.semifinishedType_name,
                    semifinished_id=self.instance.semifinished_id,
                    semifinished_code=self.instance.semifinished_code,
                    semifinished_name=self.instance.semifinished_name,
                    batch=self.instance.batch,
                    sum=self.instance.sum,
                    attribute1=self.instance.attribute1,
                    attribute2=self.instance.attribute2,
                    attribute3=self.instance.attribute3,
                    attribute4=self.instance.attribute4,
                    attribute5=self.instance.attribute5)
        if state == "作废" and self.instance.state == "审核中" :  # 如果审核过程中报废信息
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()

    # 增加操作  条件判断
    def increase(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'semifinished_id__iexact' : self.instance.semifinished_id,
                     'position_id__iexact' : self.instance.position_id,
                     'batch__iexact' : self.instance.batch
                     }
        if state == "作废" :
            return
        try :
            semifinishedStockDetail = SemifinishedStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if (self.instance.sum + semifinishedStockDetail.sum) > position.maximum :  # 如果操作数量+库存数量 超出库存数量
                raise serializers.ValidationError("当前增加数量加库存数量超出仓位最大容量")
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'semifinished_id__iexact' : self.instance.semifinished_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                semifinishedStockInfor = SemifinishedStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            semifinishedStockInfor.sum += self.instance.sum  # 更新库存数量
            semifinishedStockInfor.save()
            semifinishedStockDetail.sum += self.instance.sum  # 更新库存数量
            semifinishedStockDetail.save()

    # 出库操作 条件判断
    # def outbound(self, state) :
    #     condtions = {'state__iexact' : "使用中",
    #                  'semifinished_id__iexact' : self.instance.semifinished_id,
    #                  'position_id__iexact' : self.instance.position_id,
    #                  'batch__iexact' : self.instance.batch
    #                  }
    #     if state == "作废" :
    #         return
    #     try :
    #         semifinishedStockDetail = SemifinishedStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
    #     except Exception as e :
    #         raise serializers.ValidationError("当前库存明细不存在,无法进行出库操作")
    #     position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
    #     if state == "审核中" or state == "完成":  # 提交情况下
    #         if self.instance.sum > semifinishedStockDetail.sum :  # 如果操作数量超出库存数量
    #             raise serializers.ValidationError("当前出库数量超出库存数量")
    #     if state == "完成" :  # 通过审核情况下
    #         condtions1 = {'semifinished_id__iexact' : self.instance.semifinished_id,
    #                       'warehouse_code__iexact' : self.instance.warehouse_code,
    #                       'batch__iexact' : self.instance.batch
    #                       }
    #         try :
    #             semifinishedStockInfor = SemifinishedStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
    #         except Exception as e :
    #             raise serializers.ValidationError("当前库存信息与库存明细不符合")
    #         semifinishedStockInfor.sum -= self.instance.sum  # 更新库存数量
    #         semifinishedStockInfor.save()
    #         semifinishedStockDetail.sum -= self.instance.sum  # 更新库存数量
    #         semifinishedStockDetail.save()
    #         if (semifinishedStockDetail.sum <= 0) :
    #             position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
    #             position.save()
    #             semifinishedStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
    #             semifinishedStockDetail.save()

    def outbound(self, state):
        condtions = {'state__iexact': "使用中",
                     'semifinished_id__iexact': self.instance.semifinished_id,
                     'position_id__iexact': self.instance.position_id,
                     'batch__iexact': self.instance.batch
                     }
        try:
            semifinishedStockDetail = SemifinishedStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e:
            raise serializers.ValidationError("当前库存明细不存在,无法进行出库操作")
        condtions1 = {'semifinished_id__iexact': self.instance.semifinished_id,
                      'warehouse_code__iexact': self.instance.warehouse_code,
                      'batch__iexact': self.instance.batch
                      }
        try:
            semifinishedStockInfor = SemifinishedStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
        except Exception as e:
            raise serializers.ValidationError("当前库存信息与库存明细不符合")
        if (self.instance.state == "新建" and state == "作废"):
            return
        if (self.instance.state == "新建" and state == "审核中"):  # 提交情况下
            if self.instance.sum > semifinishedStockDetail.sum:  # 如果操作数量超出库存数量
                raise serializers.ValidationError("当前出库数量超出库存数量")
            semifinishedStockInfor.sum -= self.instance.sum  # 更新库存数量
            semifinishedStockInfor.save()
            semifinishedStockDetail.sum -= self.instance.sum  # 更新库存数量
            semifinishedStockDetail.save()
        if (self.instance.state == "审核中" and state == "完成"):  # 通过审核情况下
            position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
            if (semifinishedStockDetail.sum <= 0):
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                semifinishedStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                semifinishedStockDetail.save()
        if (self.instance.state == "审核中" and state == "新建"):  # 驳回情况下
            semifinishedStockInfor.sum += self.instance.sum  # 更新库存数量
            semifinishedStockInfor.save()
            semifinishedStockDetail.sum += self.instance.sum  # 更新库存数量
            semifinishedStockDetail.save()
        if (self.instance.state == "审核中" and state == "作废"):  # 审核作废情况下
            semifinishedStockInfor.sum += self.instance.sum  # 更新库存数量
            semifinishedStockInfor.save()
            semifinishedStockDetail.sum += self.instance.sum  # 更新库存数量
            semifinishedStockDetail.save()
    # 盘点操作 条件判断
    def inventory(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'semifinished_id__iexact' : self.instance.semifinished_id,
                     'position_id__iexact' : self.instance.position_id,
                     'batch__iexact' : self.instance.batch
                     }
        if state == "作废" :
            return
        try :
            semifinishedStockDetail = SemifinishedStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'semifinished_id__iexact' : self.instance.semifinished_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                semifinishedStockInfor = SemifinishedStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            semifinishedStockInfor.sum += self.instance.sum  # 更新库存数量
            semifinishedStockInfor.save()
            semifinishedStockDetail.sum += self.instance.sum  # 更新库存数量
            semifinishedStockDetail.save()
            if (semifinishedStockDetail.sum <= 0) :
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                semifinishedStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                semifinishedStockDetail.save()

    # 所有字段验证
    def validate(self, attrs) :
        try :
            del attrs['alter']  # 删除alter字段
        except Exception :
            pass
        if self.instance.type == "增加操作" :
            self.increase(attrs['state'])
        elif self.instance.type == "入库操作" or self.instance.type == "退库操作" :
            self.storage(attrs['state'])
        elif self.instance.type == "出库操作" :
            self.outbound(attrs['state'])
        elif self.instance.type == "盘点操作" :
            self.inventory(attrs['state'])
        return attrs

    # 状态字段验证
    def validate_state(self, value) :
        if (self.instance.create_user == self.context['request'].user.username) and \
                (self.instance.auditor != self.context['request'].user.username) :  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")) :
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "新建" and \
                (value == "审核中" or value == "作废")) :
            return value
        if (self.instance.state == "审核中" and \
                (value == "完成" or value == "新建" or value == "作废")) :
            return value
        if (self.instance.state == "完成" and \
                (value == "作废")) :
            return value
        raise serializers.ValidationError("不能从" + self.instance.state + "更新到" + value)
        return value

    # 审核记录字段验证
    def validate_alter(self, value) :
        obj = SemifinishedManageModel.objects.get(id=self.instance.id).alter
        for data in value :
            obj.add(data.id)
        return value


# endregion

# region 产品管理  序列化器

class ProductManageSerialize_Create(serializers.ModelSerializer) :
    """
    产品管理--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = ProductManageModel
        fields = ("id", "name", "code", "state", "type", "position_id", "product_id", "inspectionReport_id","handler", "batch",
                  "sum", "dataTime", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "file", "desc", "create_user", "auditor"
                  )

    # 所有字段验证
    def validate(self, attrs) :
        if not attrs["create_user"].has_perm('warehouse.add_productmanagemodel') :  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True :
            if attrs["create_user"].username == attrs["auditor"] :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            product = ProductInforDefinitionModel.objects.get(id=attrs["product_id"])  # 判断指定的产品是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的产品不存在")
        if product.state != "使用中" :
            raise serializers.ValidationError("指定的产品不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["productType_code"] = product.type.code  # 获取产品类型编码
        attrs["productType_name"] = product.type.name  # 获取产品类型名称
        attrs["product_code"] = product.code  # 获取产品编码
        attrs["product_name"] = product.name  # 获取产品名称
        if 'inspectionReport_id' in attrs.keys():
            if attrs['inspectionReport_id'] is not '':
                try:
                    report = InspectionReportModel.objects.get(id=attrs["inspectionReport_id"])  # 判断指定的质检报告是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的质检报告不存在")
                attrs["inspectionReportType_code"] = report.type.code  # 获取质检报告类型编码
                attrs["inspectionReportType_name"] = report.type.name  # 获取质检报告类型名称
                attrs["inspectionReport_code"] = report.code  # 获取质检报告编码
                attrs["inspectionReport_name"] = report.name  # 获取质检报告名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_productmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class ProductManageSerialize_List(serializers.ModelSerializer) :
    """
    产品管理--list
    """

    class Meta :
        model = ProductManageModel
        fields = (
        "id", "name", "code", "state", "type", "warehouse_code", "warehouse_name", "position_code", "position_name",
        "product_code", "product_name", "handler", "batch", "sum", "dataTime", "auditor", "create_user","create_time","update_time")


class ProductManageSerialize_Retrieve(serializers.ModelSerializer) :
    """
    产品管理--retrieve
    """
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta :
        model = ProductManageModel
        fields = "__all__"


class ProductManageSerialize_Update(serializers.ModelSerializer) :
    """
    产品管理--update
    """

    class Meta :
        model = ProductManageModel
        fields = ("id", "name", "code", "type", "position_id", "product_id", "inspectionReport_id","handler", "batch",
                  "sum", "dataTime", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor",)

    # 所有字段验证
    def validate(self, attrs) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        try :
            position = PositionDefinitionModel.objects.get(id=attrs["position_id"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓位不存在")
        try :
            product = ProductInforDefinitionModel.objects.get(id=attrs["product_id"])  # 判断指定的产品是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的产品不存在")
        if product.state != "使用中" :
            raise serializers.ValidationError("指定的产品不在'使用中'状态")
        attrs["warehouse_code"] = position.type.code  # 获取仓库编码
        attrs["warehouse_name"] = position.type.name  # 获取仓库名称
        attrs["position_code"] = position.code  # 获取仓位编码
        attrs["position_name"] = position.name  # 获取仓位名称
        attrs["productType_code"] = product.type.code  # 获取产品类型编码
        attrs["productType_name"] = product.type.name  # 获取产品类型名称
        attrs["product_code"] = product.code  # 获取产品编码
        attrs["product_name"] = product.name  # 获取产品名称
        if 'inspectionReport_id' in attrs.keys():
            if attrs['inspectionReport_id'] is not '':
                try:
                    report = InspectionReportModel.objects.get(id=attrs["inspectionReport_id"])  # 判断指定的质检报告是否存在
                except Exception as e:
                    raise serializers.ValidationError("指定的质检报告不存在")
                attrs["inspectionReportType_code"] = report.type.code  # 获取质检报告类型编码
                attrs["inspectionReportType_name"] = report.type.name  # 获取质检报告类型名称
                attrs["inspectionReport_code"] = report.code  # 获取质检报告编码
                attrs["inspectionReport_name"] = report.name  # 获取质检报告名称
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True :
            if self.instance.create_user == value :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_productmanagemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class ProductManageSerialize_Partial(serializers.ModelSerializer) :
    """
    产品管理--partial
    """

    class Meta :
        model = ProductManageModel
        fields = ("id", "state", "alter")

    # 入库操作/退库操作条件判断
    def storage(self, state) :
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if position.state != "闲置" :  # 如果指定的仓位不处于‘空闲状态’
                raise serializers.ValidationError("当前仓位不在‘空闲状态’")
            if self.instance.sum > position.maximum :  # 如果操作数量超出了仓位最大容量
                raise serializers.ValidationError("操作数量超出了仓位的最大容量’")
            position.state = "使用中"  # 占用当前仓位(将状态置为‘使用中状态’)
            position.save()
        if state == "新建" :  # 驳回情况下
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()
        if state == "完成" :  # 通过审核情况下
            ProductStockDetailModel.objects.create(  # 新建一条库存记录
                state="使用中",
                warehouse_code=self.instance.warehouse_code,
                warehouse_name=self.instance.warehouse_name,
                position_id=self.instance.position_id,
                position_code=self.instance.position_code,
                position_name=self.instance.position_name,
                productType_code=self.instance.productType_code,
                productType_name=self.instance.productType_name,
                product_id=self.instance.product_id,
                product_code=self.instance.product_code,
                product_name=self.instance.product_name,
                batch=self.instance.batch,
                sum=self.instance.sum,
                attribute1=self.instance.attribute1,
                attribute2=self.instance.attribute2,
                attribute3=self.instance.attribute3,
                attribute4=self.instance.attribute4,
                attribute5=self.instance.attribute5)
            condtions1 = {'product_id__iexact' : self.instance.product_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                productStockInfor = ProductStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
                productStockInfor.sum += self.instance.sum  # 更新库存数量
                productStockInfor.save()
            except Exception as e :
                ProductStockInforModel.objects.create(  # 新建一条库存记录
                    warehouse_code=self.instance.warehouse_code,
                    warehouse_name=self.instance.warehouse_name,
                    productType_code=self.instance.productType_code,
                    productType_name=self.instance.productType_name,
                    product_id=self.instance.product_id,
                    product_code=self.instance.product_code,
                    product_name=self.instance.product_name,
                    batch=self.instance.batch,
                    sum=self.instance.sum,
                    attribute1=self.instance.attribute1,
                    attribute2=self.instance.attribute2,
                    attribute3=self.instance.attribute3,
                    attribute4=self.instance.attribute4,
                    attribute5=self.instance.attribute5)
        if state == "作废" and self.instance.state == "审核中" :  # 如果审核过程中报废信息
            position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
            position.save()

    # 增加操作  条件判断
    def increase(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'product_id__iexact' : self.instance.product_id,
                     'position_id__iexact' : self.instance.position_id,
                     'batch__iexact' : self.instance.batch
                     }
        if state == "作废" :
            return
        try :
            productStockDetail = ProductStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "审核中" :  # 提交情况下
            if (self.instance.sum + productStockDetail.sum) > position.maximum :  # 如果操作数量+库存数量 超出库存数量
                raise serializers.ValidationError("当前增加数量加库存数量超出仓位最大容量")
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'product_id__iexact' : self.instance.product_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                productStockInfor = ProductStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            productStockInfor.sum += self.instance.sum  # 更新库存数量
            productStockInfor.save()
            productStockDetail.sum += self.instance.sum  # 更新库存数量
            productStockDetail.save()

    # # 出库操作 条件判断
    # def outbound(self, state) :
    #     condtions = {'state__iexact' : "使用中",
    #                  'product_id__iexact' : self.instance.product_id,
    #                  'position_id__iexact' : self.instance.position_id,
    #                  'batch__iexact' : self.instance.batch
    #                  }
    #     if state == "作废" :
    #         return
    #     try :
    #         productStockDetail = ProductStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
    #     except Exception as e :
    #         raise serializers.ValidationError("当前库存明细不存在,无法进行出库操作")
    #     if state == "审核中" or state == "完成":  # 提交情况下
    #         if self.instance.sum > productStockDetail.sum :  # 如果操作数量超出库存数量
    #             raise serializers.ValidationError("当前出库数量超出库存数量")
    #     if state == "完成" :  # 通过审核情况下
    #         condtions1 = {'product_id__iexact' : self.instance.product_id,
    #                       'warehouse_code__iexact' : self.instance.warehouse_code,
    #                       'batch__iexact' : self.instance.batch
    #                       }
    #         try :
    #             productStockInfor = ProductStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
    #         except Exception as e :
    #             raise serializers.ValidationError("当前库存信息与库存明细不符合")
    #         position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
    #         productStockInfor.sum -= self.instance.sum  # 更新库存数量
    #         productStockInfor.save()
    #         productStockDetail.sum -= self.instance.sum  # 更新库存数量
    #         productStockDetail.save()
    #         if (productStockDetail.sum <= 0) :
    #             position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
    #             position.save()
    #             productStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
    #             productStockDetail.save()
    # 出库操作 条件判断
    def outbound(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'product_id__iexact' : self.instance.product_id,
                     'position_id__iexact' : self.instance.position_id,
                     'batch__iexact' : self.instance.batch
                     }
        try :
            productStockDetail = ProductStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行出库操作")
        condtions1 = {'product_id__iexact': self.instance.product_id,
                      'warehouse_code__iexact': self.instance.warehouse_code,
                      'batch__iexact': self.instance.batch
                      }
        try:
            productStockInfor = ProductStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
        except Exception as e:
            raise serializers.ValidationError("当前库存信息与库存明细不符合")
        if (self.instance.state == "新建" and state == "作废"):
            return
        if (self.instance.state=="新建" and state == "审核中"):  # 提交情况下
            if self.instance.sum > productStockDetail.sum :  # 如果操作数量超出库存数量
                raise serializers.ValidationError("当前出库数量超出库存数量")
            productStockInfor.sum -= self.instance.sum  # 更新库存数量
            productStockInfor.save()
            productStockDetail.sum -= self.instance.sum  # 更新库存数量
            productStockDetail.save()
        if (self.instance.state=="审核中" and state == "完成"):  # 通过审核情况下
            position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
            if (productStockDetail.sum <= 0) :
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                productStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                productStockDetail.save()
        if (self.instance.state=="审核中" and state == "新建"):  # 驳回情况下
            productStockInfor.sum += self.instance.sum  # 更新库存数量
            productStockInfor.save()
            productStockDetail.sum += self.instance.sum  # 更新库存数量
            productStockDetail.save()
        if (self.instance.state=="审核中" and state == "作废"):  # 审核作废情况下
            productStockInfor.sum += self.instance.sum  # 更新库存数量
            productStockInfor.save()
            productStockDetail.sum += self.instance.sum  # 更新库存数量
            productStockDetail.save()

    # 盘点操作 条件判断
    def inventory(self, state) :
        condtions = {'state__iexact' : "使用中",
                     'product_id__iexact' : self.instance.product_id,
                     'position_id__iexact' : self.instance.position_id,
                     'batch__iexact' : self.instance.batch
                     }
        if state == "作废" :
            return
        try :
            productStockDetail = ProductStockDetailModel.objects.get(**condtions)  # 获取指定的库存明细
        except Exception as e :
            raise serializers.ValidationError("当前库存明细不存在,无法进行增加操作")
        position = PositionDefinitionModel.objects.get(id=self.instance.position_id)  # 获取指定的仓位信息
        if state == "完成" :  # 通过审核情况下
            condtions1 = {'product_id__iexact' : self.instance.product_id,
                          'warehouse_code__iexact' : self.instance.warehouse_code,
                          'batch__iexact' : self.instance.batch
                          }
            try :
                productStockInfor = ProductStockInforModel.objects.get(**condtions1)  # 获取指定的库存信息
            except Exception as e :
                raise serializers.ValidationError("当前库存信息与库存明细不符合")
            productStockInfor.sum += self.instance.sum  # 更新库存数量
            productStockInfor.save()
            productStockDetail.sum += self.instance.sum  # 更新库存数量
            productStockDetail.save()
            if (productStockDetail.sum <= 0) :
                position.state = "闲置"  # 释放当前仓位(将状态置为‘空闲状态’)
                position.save()
                productStockDetail.state = "完成"  # 释放当前库存明细(将状态置为‘空闲状态’)
                productStockDetail.save()

    # 所有字段验证
    def validate(self, attrs) :
        try :
            del attrs['alter']  # 删除alter字段
        except Exception :
            pass
        if self.instance.type == "增加操作" :
            self.increase(attrs['state'])
        elif self.instance.type == "入库操作" or self.instance.type == "退库操作" :
            self.storage(attrs['state'])
        elif self.instance.type == "出库操作" :
            self.outbound(attrs['state'])
        elif self.instance.type == "盘点操作" :
            self.inventory(attrs['state'])
        return attrs

    # 状态字段验证
    def validate_state(self, value) :
        if (self.instance.create_user == self.context['request'].user.username) and \
                (self.instance.auditor != self.context['request'].user.username) :  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")) :
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        if (self.instance.state == "新建" and \
                (value == "审核中" or value == "作废")) :
            return value
        if (self.instance.state == "审核中" and \
                (value == "完成" or value == "新建" or value == "作废")) :
            return value
        if (self.instance.state == "完成" and \
                (value == "作废")) :
            return value
        raise serializers.ValidationError("不能从" + self.instance.state + "更新到" + value)
        return value

    # 审核记录字段验证
    def validate_alter(self, value) :
        obj = ProductManageModel.objects.get(id=self.instance.id).alter
        for data in value :
            obj.add(data.id)
        return value


# endregion

# region 物料预警规则子项创建 序列化器
class MaterialWaringRuleItemSerialize_Create(serializers.ModelSerializer) :
    """
    物料预警规则子项创建--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = MaterialWaringRuleItemModel
        fields = ("id", "warehouse_code", "material_id", "batch", "minimum", "maximum",
                  "lowthreshold", "highthreshold", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user")

    def validate(self, attrs) :
        try :
            warehouse = WarehouseDefinitionModel.objects.get(code=attrs["warehouse_code"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓库不存在")
        try :
            material = MaterialInforDefinitionModel.objects.get(id=attrs["material_id"])  # 判断指定的物料是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的物料不存在")
        attrs["warehouse_name"] = warehouse.name  # 获取仓库名称
        attrs["materialType_code"] = material.type.code  # 获取物料类型编码
        attrs["materialType_name"] = material.type.name  # 获取物料类型名称
        attrs["material_code"] = material.code  # 获取物料编码
        attrs["material_name"] = material.name  # 获取物料名称
        return attrs


class MaterialWaringRuleItemSerialize_List(serializers.ModelSerializer) :
    """
    物料预警规则子项创建--list
    """

    class Meta :
        model = MaterialWaringRuleItemModel
        fields = "__all__"


# endregion

# region 物料预警规则创建 序列化器
class MaterialWaringRuleSerialize_Create(serializers.ModelSerializer) :
    """
    物料预警规则创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = MaterialWaringRuleModel
        fields = ("id", "name", "code", "state", "file", "child", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs) :
        if not attrs["create_user"].has_perm('warehouse.add_materialwaringrulemodel') :  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True :
            if attrs["create_user"].username == attrs["auditor"] :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_materialwaringrulemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class MaterialWaringRuleSerialize_List(serializers.ModelSerializer) :
    """
    物料预警规则创建--list
    """

    class Meta :
        model = MaterialWaringRuleModel
        fields = ("id", "name", "code", "state", "auditor", "create_user","create_time","update_time")


class MaterialWaringRuleSerialize_Retrieve(serializers.ModelSerializer) :
    """
    物料预警规则创建--retrieve
    """
    file = WarehouseFileSerialize_List(many=True)
    child = MaterialWaringRuleItemSerialize_List(many=True)
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta :
        model = MaterialWaringRuleModel
        fields = "__all__"


class MaterialWaringRuleSerialize_Update(serializers.ModelSerializer) :
    """
    物料预警规则创建--update
    """

    class Meta :
        model = MaterialWaringRuleModel
        fields = ("id", "name", "code", "file", "child", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor")

    # 所有字段验证
    def validate(self, attrs) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True :
            if self.instance.create_user == value :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_materialwaringrulemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class MaterialWaringRuleSerialize_Partial(serializers.ModelSerializer) :
    """
    物料预警规则创建--partial
    """

    class Meta :
        model = MaterialWaringRuleModel
        fields = ("id", "state", "alter")

    # 所有字段验证
    def validate(self, attrs) :
        try :
            del attrs['alter']  # 删除alter字段
        except Exception :
            pass
        return attrs

    # 状态字段验证
    def validate_state(self, value) :
        validate_states(self.instance.state, value)
        if (self.instance.create_user == self.context['request'].user.username) and \
                (self.instance.auditor != self.context['request'].user.username) :  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")) :
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value) :
        obj = MaterialWaringRuleModel.objects.get(id=self.instance.id).alter
        for data in value :
            obj.add(data.id)
        return value


# endregion

# region 半成品预警规则子项创建 序列化器
class SemifinishedWaringRuleItemSerialize_Create(serializers.ModelSerializer) :
    """
    半成品预警规则子项创建--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = SemifinishedWaringRuleItemModel
        fields = ("id", "warehouse_code", "semifinished_id", "batch", "minimum", "maximum",
                  "lowthreshold", "highthreshold", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user")

    def validate(self, attrs) :
        try :
            warehouse = WarehouseDefinitionModel.objects.get(code=attrs["warehouse_code"])  # 判断指定的仓位是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓库不存在")
        try :
            semifinished = SemifinishedInforDefinitionModel.objects.get(id=attrs["semifinished_id"])  # 判断指定的半成品是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的半成品不存在")
        attrs["warehouse_name"] = warehouse.name  # 获取仓库名称
        attrs["semifinishedType_code"] = semifinished.type.code  # 获取半成品类型编码
        attrs["semifinishedType_name"] = semifinished.type.name  # 获取半成品类型名称
        attrs["semifinished_code"] = semifinished.code  # 获取半成品编码
        attrs["semifinished_name"] = semifinished.name  # 获取半成品名称
        return attrs


class SemifinishedWaringRuleItemSerialize_List(serializers.ModelSerializer) :
    """
    半成品预警规则子项创建--list
    """

    class Meta :
        model = SemifinishedWaringRuleItemModel
        fields = "__all__"


# endregion

# region 半成品预警规则创建 序列化器
class SemifinishedWaringRuleSerialize_Create(serializers.ModelSerializer) :
    """
    半成品预警规则创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = SemifinishedWaringRuleModel
        fields = ("id", "name", "code", "state", "file", "child", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs) :
        if not attrs["create_user"].has_perm('warehouse.add_semifinishedwaringrulemodel') :  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True :
            if attrs["create_user"].username == attrs["auditor"] :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_semifinishedwaringrulemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class SemifinishedWaringRuleSerialize_List(serializers.ModelSerializer) :
    """
    半成品预警规则创建--list
    """

    class Meta :
        model = SemifinishedWaringRuleModel
        fields = ("id", "name", "code", "state", "auditor", "create_user","create_time","update_time")


class SemifinishedWaringRuleSerialize_Retrieve(serializers.ModelSerializer) :
    """
    半成品预警规则创建--retrieve
    """
    file = WarehouseFileSerialize_List(many=True)
    child = SemifinishedWaringRuleItemSerialize_List(many=True)
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta :
        model = SemifinishedWaringRuleModel
        fields = "__all__"


class SemifinishedWaringRuleSerialize_Update(serializers.ModelSerializer) :
    """
    半成品预警规则创建--update
    """

    class Meta :
        model = SemifinishedWaringRuleModel
        fields = ("id", "name", "code", "file", "child", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor")

    # 所有字段验证
    def validate(self, attrs) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True :
            if self.instance.create_user == value :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_semifinishedwaringrulemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class SemifinishedWaringRuleSerialize_Partial(serializers.ModelSerializer) :
    """
    半成品预警规则创建--partial
    """

    class Meta :
        model = SemifinishedWaringRuleModel
        fields = ("id", "state", "alter")

    # 所有字段验证
    def validate(self, attrs) :
        try :
            del attrs['alter']  # 删除alter字段
        except Exception :
            pass
        return attrs

    # 状态字段验证
    def validate_state(self, value) :
        validate_states(self.instance.state, value)
        if (self.instance.create_user == self.context['request'].user.username) and \
                (self.instance.auditor != self.context['request'].user.username) :  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")) :
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value) :
        obj = SemifinishedWaringRuleModel.objects.get(id=self.instance.id).alter
        for data in value :
            obj.add(data.id)
        return value


# endregion

# region 产品预警规则子项创建 序列化器
class ProductWaringRuleItemSerialize_Create(serializers.ModelSerializer) :
    """
    产品预警规则子项创建--create
    """
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = ProductWaringRuleItemModel
        fields = ("id", "warehouse_code", "product_id", "batch", "minimum", "maximum",
                  "lowthreshold", "highthreshold", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "create_user")

    def validate(self, attrs) :
        try :
            warehouse = WarehouseDefinitionModel.objects.get(code=attrs["warehouse_code"])  # 判断指定的仓库是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的仓库不存在")
        try :
            product = ProductInforDefinitionModel.objects.get(id=attrs["product_id"])  # 判断指定的产品是否存在
        except Exception as e :
            raise serializers.ValidationError("指定的产品不存在")
        attrs["warehouse_name"] = warehouse.name  # 获取仓库名称
        attrs["productType_code"] = product.type.code  # 获取产品类型编码
        attrs["productType_name"] = product.type.name  # 获取产品类型名称
        attrs["product_code"] = product.code  # 获取产品编码
        attrs["product_name"] = product.name  # 获取产品名称
        return attrs


class ProductWaringRuleItemSerialize_List(serializers.ModelSerializer) :
    """
    产品预警规则子项创建--list
    """

    class Meta :
        model = ProductWaringRuleItemModel
        fields = "__all__"


# endregion

# region 产品预警规则创建 序列化器
class ProductWaringRuleSerialize_Create(serializers.ModelSerializer) :
    """
    产品预警规则创建--create
    """
    state = serializers.HiddenField(default="新建")
    create_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta :
        model = ProductWaringRuleModel
        fields = ("id", "name", "code", "state", "file", "child", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor", "create_user")

    # 所有字段验证
    def validate(self, attrs) :
        if not attrs["create_user"].has_perm('warehouse.add_productwaringrulemodel') :  # 如果当前用户没有创建权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        if settings.SAME_USER != True :
            if attrs["create_user"].username == attrs["auditor"] :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_productwaringrulemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class ProductWaringRuleSerialize_List(serializers.ModelSerializer) :
    """
    产品预警规则创建--list
    """

    class Meta :
        model = ProductWaringRuleModel
        fields = ("id", "name", "code", "state", "auditor", "create_user","create_time","update_time")


class ProductWaringRuleSerialize_Retrieve(serializers.ModelSerializer) :
    """
    产品预警规则创建--retrieve
    """
    file = WarehouseFileSerialize_List(many=True)
    child = ProductWaringRuleItemSerialize_List(many=True)
    alter = WarehouseAlterRecordSerialize_List(many=True)

    class Meta :
        model = ProductWaringRuleModel
        fields = "__all__"


class ProductWaringRuleSerialize_Update(serializers.ModelSerializer) :
    """
    产品预警规则创建--update
    """

    class Meta :
        model = ProductWaringRuleModel
        fields = ("id", "name", "code", "file", "child", "attribute1", "attribute2",
                  "attribute3", "attribute4", "attribute5", "desc", "auditor")

    # 所有字段验证
    def validate(self, attrs) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        return attrs

    # 审核者字段验证
    def validate_auditor(self, value) :
        if self.instance.state != '新建' :  # 如果不是新建状态 不能更改信息
            raise serializers.ValidationError("当前信息已提交,禁止更改")
        if settings.SAME_USER != True :
            if self.instance.create_user == value :  # 审核帐号不能与创建帐号相同
                raise serializers.ValidationError("审核帐号不能与创建帐号相同'")
        try :
            auditor = User.objects.get(username=value)
        except Exception as e :
            raise serializers.ValidationError("指定的审核账号不存在")
        if not auditor.has_perm('warehouse.admin_productwaringrulemodel') :
            raise serializers.ValidationError("指定的审核账号不具备审核权限")
        return value


class ProductWaringRuleSerialize_Partial(serializers.ModelSerializer) :
    """
    产品预警规则创建--partial
    """

    class Meta :
        model = ProductWaringRuleModel
        fields = ("id", "state", "alter")

    # 所有字段验证
    def validate(self, attrs) :
        try :
            del attrs['alter']  # 删除alter字段
        except Exception :
            pass
        return attrs

    # 状态字段验证
    def validate_state(self, value) :
        validate_states(self.instance.state, value)
        if (self.instance.create_user == self.context['request'].user.username) and \
                (self.instance.auditor != self.context['request'].user.username) :  # 如果当前用户为创建账号但不是审核账号
            if not (self.instance.state == "新建" and (value == "审核中" or value == "作废")) :
                raise serializers.ValidationError("创建者只能将[新建]信息更改成[审核中]或[作废]")
        return value

    # 审核记录字段验证
    def validate_alter(self, value) :
        obj = ProductWaringRuleModel.objects.get(id=self.instance.id).alter
        for data in value :
            obj.add(data.id)
        return value

# endregion
