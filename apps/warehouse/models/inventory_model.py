from django.db import models
from .basicinfor_model import *

class EquipmentStockDetailModel(models.Model) :
    """
    设备库存明细
    """
    STATUS = (
        ("使用中", "使用中"),
        ("完成", "完成"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16, choices=STATUS, default="使用中", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="设备放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="设备放置的仓库名称")
    position_id = models.CharField(max_length=16, name="position_id", verbose_name="仓位id", help_text="设备放置的仓位id")
    position_code = models.CharField(max_length=32, name="position_code", verbose_name="仓位编码", help_text="设备放置的仓位编码")
    position_name = models.CharField(max_length=32, name="position_name", verbose_name="仓位名称", help_text="设备放置的仓位名称")
    equipmentType_code = models.CharField(max_length=32, name="equipmentType_code", verbose_name="设备类型编码",
                                         help_text="当前物品的设备类型编码")
    equipmentType_name = models.CharField(max_length=32, name="equipmentType_name", verbose_name="设备类型名称",
                                         help_text="当前物品的设备类型名称")
    equipment_id = models.CharField(max_length=16, name="equipment_id", verbose_name="设备id", help_text="当前物品的设备id")
    equipment_code = models.CharField(max_length=32, name="equipment_code", verbose_name="设备编码", help_text="当前物品的设备编码")
    equipment_name = models.CharField(max_length=32, name="equipment_name", verbose_name="设备名称", help_text="当前物品的设备名称")
    sum = models.IntegerField(name="sum", verbose_name="库存数量", help_text="当前设备库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self) :
        return (self.equipment_code + "  >>  " + self.equipment_name)

    class Meta :
        db_table = "EquipmentStockDetailModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－设备库存明细"
        verbose_name_plural = verbose_name
class PartsStockDetailModel(models.Model) :
    """
    设备配件库存明细
    """
    STATUS = (
        ("使用中", "使用中"),
        ("完成", "完成"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16, choices=STATUS, default="使用中", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="设备配件放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="设备配件放置的仓库名称")
    position_id = models.CharField(max_length=16, name="position_id", verbose_name="仓位id", help_text="设备配件放置的仓位id")
    position_code = models.CharField(max_length=32, name="position_code", verbose_name="仓位编码", help_text="设备配件放置的仓位编码")
    position_name = models.CharField(max_length=32, name="position_name", verbose_name="仓位名称", help_text="设备配件放置的仓位名称")
    partsType_code = models.CharField(max_length=32, name="partsType_code", verbose_name="设备配件类型编码",
                                         help_text="当前物品的设备配件类型编码")
    partsType_name = models.CharField(max_length=32, name="partsType_name", verbose_name="设备配件类型名称",
                                         help_text="当前物品的设备配件类型名称")
    parts_id = models.CharField(max_length=16, name="parts_id", verbose_name="设备配件id", help_text="当前物品的设备配件id")
    parts_code = models.CharField(max_length=32, name="parts_code", verbose_name="设备配件编码", help_text="当前物品的设备配件编码")
    parts_name = models.CharField(max_length=32, name="parts_name", verbose_name="设备配件名称", help_text="当前物品的设备配件名称")
    sum = models.IntegerField(name="sum", verbose_name="库存数量", help_text="当前设备配件库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self) :
        return (self.parts_code + "  >>  " + self.parts_name)

    class Meta :
        db_table = "PartsStockDetailModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－设备配件库存明细"
        verbose_name_plural = verbose_name


class MaterialStockDetailModel(models.Model):
    """
    物料库存明细
    """
    STATUS = (
        ("使用中", "使用中"),
        ("完成", "完成"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16,choices=STATUS, default="使用中", name="state", verbose_name="状态", help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="物料放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="物料放置的仓库名称")
    position_id = models.CharField(max_length=16,  name="position_id", verbose_name="仓位id", help_text="物料放置的仓位id")
    position_code = models.CharField(max_length=32,  name="position_code", verbose_name="仓位编码", help_text="物料放置的仓位编码")
    position_name = models.CharField(max_length=32,  name="position_name", verbose_name="仓位名称", help_text="物料放置的仓位名称")
    materialType_code = models.CharField(max_length=32, name="materialType_code", verbose_name="物料类型编码", help_text="当前物品的物料类型编码")
    materialType_name = models.CharField(max_length=32,  name="materialType_name", verbose_name="物料类型名称",help_text="当前物品的物料类型名称")
    material_id = models.CharField(max_length=16, name="material_id", verbose_name="物料id", help_text="当前物品的物料id")
    material_code = models.CharField(max_length=32, name="material_code", verbose_name="物料编码", help_text="当前物品的物料编码")
    material_name = models.CharField(max_length=32,  name="material_name", verbose_name="物料名称",help_text="当前物品的物料名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="物料批次", help_text="当前物料的批次")
    sum = models.IntegerField( name="sum",verbose_name="库存数量", help_text="当前物料库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self):
        return (self.material_code + "  >>  "+ self.material_name)

    class Meta:
        db_table = "MaterialStockDetailModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－物料库存明细"
        verbose_name_plural = verbose_name

class SemifinishedStockDetailModel(models.Model):
    """
    半成品库存明细
    """
    STATUS = (
        ("使用中", "使用中"),
        ("完成", "完成"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16,choices=STATUS, default="使用中", name="state", verbose_name="状态", help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="半成品放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="半成品放置的仓库名称")
    position_id = models.CharField(max_length=16,  name="position_id", verbose_name="仓位id", help_text="半成品放置的仓位id")
    position_code = models.CharField(max_length=32,  name="position_code", verbose_name="仓位编码", help_text="半成品放置的仓位编码")
    position_name = models.CharField(max_length=32,  name="position_name", verbose_name="仓位名称", help_text="半成品放置的仓位名称")
    semifinishedType_code = models.CharField(max_length=32, name="semifinishedType_code", verbose_name="半成品类型编码",
                                         help_text="当前物品的半成品类型编码")
    semifinishedType_name = models.CharField(max_length=32, name="semifinishedType_name", verbose_name="半成品类型名称",
                                         help_text="当前物品的半成品类型名称")
    semifinished_id = models.CharField(max_length=16, name="semifinished_id", verbose_name="半成品id", help_text="当前物品的半成品id")
    semifinished_code = models.CharField(max_length=32, name="semifinished_code", verbose_name="半成品编码", help_text="当前物品的半成品编码")
    semifinished_name = models.CharField(max_length=32,  name="semifinished_name", verbose_name="半成品名称",help_text="当前物品的半成品名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="半成品批次", help_text="当前半成品的批次")
    sum = models.IntegerField( name="sum", verbose_name="库存数量", help_text="当前半成品库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self):
        return (self.semifinished_code + "  >>  "+ self.semifinished_name)

    class Meta:
        db_table = "SemifinishedStockDetailModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－半成品库存明细"
        verbose_name_plural = verbose_name

class ProductStockDetailModel(models.Model):
    """
    产品库存明细
    """
    STATUS = (
        ("使用中", "使用中"),
        ("完成", "完成"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    state = models.CharField(max_length=16,choices=STATUS, default="使用中", name="state",   verbose_name="状态", help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="产品放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="产品放置的仓库名称")
    position_id = models.CharField(max_length=16,name="position_id", verbose_name="仓位id", help_text="产品放置的仓位id")
    position_code = models.CharField(max_length=32,name="position_code", verbose_name="仓位编码", help_text="产品放置的仓位编码")
    position_name = models.CharField(max_length=32,name="position_name", verbose_name="仓位名称", help_text="产品放置的仓位名称")
    productType_code = models.CharField(max_length=32, name="productType_code", verbose_name="产品类型编码", help_text="当前物品的产品类型编码")
    productType_name = models.CharField(max_length=32, name="productType_name", verbose_name="产品类型名称",help_text="当前物品的产品类型名称")
    product_id = models.CharField(max_length=16, name="product_id", verbose_name="产品id", help_text="当前物品的产品id")
    product_code = models.CharField(max_length=32, name="product_code", verbose_name="产品编码", help_text="当前物品的产品编码")
    product_name = models.CharField(max_length=32, name="product_name", verbose_name="产品名称",help_text="当前物品的产品名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="产品批次", help_text="当前产品的批次")
    sum = models.IntegerField( name="sum", verbose_name="库存数量", help_text="当前产品的库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间")

    def __str__(self):
        return (self.product_code + "  >>  "+ self.product_name)

    class Meta:
        db_table = "ProductStockDetailModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－产品库存明细"
        verbose_name_plural = verbose_name

class EquipmentStockInforModel(models.Model) :
    """
    设备库存信息
    """
    id = models.AutoField(primary_key=True, unique=True)
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="设备放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="设备放置的仓库名称")
    equipmentType_code = models.CharField(max_length=32, name="equipmentType_code", verbose_name="设备类型编码",
                                         help_text="当前物品的设备类型编码")
    equipmentType_name = models.CharField(max_length=32, name="equipmentType_name", verbose_name="设备类型名称",
                                         help_text="当前物品的设备类型名称")
    equipment_id = models.CharField(max_length=16, name="equipment_id", verbose_name="设备id", help_text="当前物品的设备id")
    equipment_code = models.CharField(max_length=32, name="equipment_code", verbose_name="设备编码", help_text="当前物品的设备编码")
    equipment_name = models.CharField(max_length=32, name="equipment_name", verbose_name="设备名称", help_text="当前物品的设备名称")
    sum = models.IntegerField(name="sum", verbose_name="库存数量", help_text="当前设备库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self) :
        return (self.equipment_code + "  >>  " + self.equipment_name)

    class Meta :
        db_table = "EquipmentStockInforModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－设备库存信息"
        verbose_name_plural = verbose_name
class PartsStockInforModel(models.Model) :
    """
    设备配件库存信息
    """
    id = models.AutoField(primary_key=True, unique=True)
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="设备配件放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="设备配件放置的仓库名称")
    partsType_code = models.CharField(max_length=32, name="partsType_code", verbose_name="设备配件类型编码",
                                         help_text="当前物品的设备配件类型编码")
    partsType_name = models.CharField(max_length=32, name="partsType_name", verbose_name="设备配件类型名称",
                                         help_text="当前物品的设备配件类型名称")
    parts_id = models.CharField(max_length=16, name="parts_id", verbose_name="设备配件id", help_text="当前物品的设备配件id")
    parts_code = models.CharField(max_length=32, name="parts_code", verbose_name="设备配件编码", help_text="当前物品的设备配件编码")
    parts_name = models.CharField(max_length=32, name="parts_name", verbose_name="设备配件名称", help_text="当前物品的设备配件名称")
    sum = models.IntegerField(name="sum", verbose_name="库存数量", help_text="当前设备配件库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self) :
        return (self.parts_code + "  >>  " + self.parts_name)

    class Meta :
        db_table = "PartsStockInforModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－设备配件库存信息"
        verbose_name_plural = verbose_name

class MaterialStockInforModel(models.Model):
    """
    物料库存信息
    """
    id = models.AutoField(primary_key=True, unique=True)
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="物料放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="物料放置的仓库名称")
    materialType_code = models.CharField(max_length=32, name="materialType_code", verbose_name="物料类型编码",help_text="当前物品的物料类型编码")
    materialType_name = models.CharField(max_length=32, name="materialType_name", verbose_name="物料类型名称",help_text="当前物品的物料类型名称")
    material_id = models.CharField(max_length=16, name="material_id", verbose_name="物料id", help_text="当前物品的物料id")
    material_code = models.CharField(max_length=32, name="material_code", verbose_name="物料编码", help_text="当前物品的物料编码")
    material_name = models.CharField(max_length=32, name="material_name", verbose_name="物料名称", help_text="当前物品的物料名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="物料批次", help_text="当前物料的批次")
    sum = models.IntegerField( name="sum",verbose_name="库存数量", help_text="当前物料库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self):
        return (self.material_code + "  >>  " + self.material_name)

    class Meta:
        db_table = "MaterialStockInforModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－物料库存信息"
        verbose_name_plural = verbose_name

class SemifinishedStockInforModel(models.Model):
    """
    半成品库存信息
    """
    id = models.AutoField(primary_key=True, unique=True)
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="半成品放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="半成品放置的仓库名称")
    semifinishedType_code = models.CharField(max_length=32, name="semifinishedType_code", verbose_name="半成品类型编码",help_text="当前物品的半成品类型编码")
    semifinishedType_name = models.CharField(max_length=32, name="semifinishedType_name", verbose_name="半成品类型名称",help_text="当前物品的半成品类型名称")
    semifinished_id = models.CharField(max_length=16, name="semifinished_id", verbose_name="半成品id", help_text="当前物品的半成品id")
    semifinished_code = models.CharField(max_length=32, name="semifinished_code", verbose_name="半成品编码", help_text="当前物品的半成品编码")
    semifinished_name = models.CharField(max_length=32, name="semifinished_name", verbose_name="半成品名称", help_text="当前物品的半成品名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="半成品批次", help_text="当前半成品的批次")
    sum = models.IntegerField( name="sum", verbose_name="库存数量", help_text="当前半成品库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self):
        return (self.semifinished_code + "  >>  " + self.semifinished_name)

    class Meta:
        db_table = "SemifinishedStockInforModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－半成品库存信息"
        verbose_name_plural = verbose_name

class ProductStockInforModel(models.Model):
    """
    产品库存信息
    """
    id = models.AutoField(primary_key=True, unique=True)
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="产品放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="产品放置的仓库名称")
    productType_code = models.CharField(max_length=32, name="productType_code", verbose_name="产品类型编码",help_text="当前物品的产品类型编码")
    productType_name = models.CharField(max_length=32, name="productType_name", verbose_name="产品类型名称",help_text="当前物品的产品类型名称")
    product_id = models.CharField(max_length=16, name="product_id", verbose_name="产品id", help_text="当前物品的产品id")
    product_code = models.CharField(max_length=32, name="product_code", verbose_name="产品编码", help_text="当前物品的产品编码")
    product_name = models.CharField(max_length=32, name="product_name", verbose_name="产品名称", help_text="当前物品的产品名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="产品批次", help_text="当前产品的批次")
    sum = models.IntegerField( name="sum", verbose_name="库存数量", help_text="当前产品库存数量")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    add_time = models.DateField(auto_now_add=True, verbose_name="创建时间", help_text="创建当前库存明细的时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前库存明细最后的更新时间")

    def __str__(self):
        return (self.product_code + "  >>  " + self.product_name)

    class Meta:
        db_table = "ProductStockInforModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－产品库存信息"
        verbose_name_plural = verbose_name

class EquipmentManageModel(models.Model) :
    """
    设备管理
    """
    OPERATING_TYPE = (
        ("增加操作", "增加操作"),
        ("入库操作", "入库操作"),
        ("退库操作", "退库操作"),
        ("出库操作", "出库操作"),
        ("盘点操作", "盘点操作"),
    )
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",
                            help_text="操作记录名称(建议唯一)")
    code = models.CharField(max_length=32, name="code", null=True, blank=True, verbose_name="编码", help_text="操作记录编码(与类型联合唯一)")
    type = models.CharField(max_length=16, choices=OPERATING_TYPE, name="type", verbose_name="类型",
                            help_text="当前操作记录属于的操作记录类型")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="设备放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="设备放置的仓库名称")
    position_id = models.CharField(max_length=16, name="position_id", verbose_name="仓位id", help_text="产品放置的仓位id")
    position_code = models.CharField(max_length=32, name="position_code", verbose_name="仓位编码", help_text="设备放置的仓位编码")
    position_name = models.CharField(max_length=32, name="position_name", verbose_name="仓位名称", help_text="设备放置的仓位名称")
    equipmentType_code = models.CharField(max_length=32, name="equipmentType_code", verbose_name="设备类型编码",
                                         help_text="当前物品的设备类型编码")
    equipmentType_name = models.CharField(max_length=32, name="EquipmentType_name", verbose_name="设备类型名称",
                                         help_text="当前物品的设备类型名称")
    equipment_id = models.CharField(max_length=16, name="equipment_id", verbose_name="设备id", help_text="当前物品的设备id")
    equipment_code = models.CharField(max_length=32, name="equipment_code", verbose_name="设备编码", help_text="当前物品的设备编码")
    equipment_name = models.CharField(max_length=32, name="equipment_name", verbose_name="设备名称", help_text="当前物品的设备名称")
    handler = models.CharField(max_length=32, name="handler", verbose_name="操作者", help_text="对当前信息进行操作的是谁")
    sum = models.IntegerField(name="sum", verbose_name="操作数量", help_text="当前操作的数量是")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="操作时间", help_text="当前操作的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前附加属性5")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="文件", help_text="当前操作的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self) :
        return self.code

    class Meta :
        db_table = "EquipmentManageModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－设备管理"
        verbose_name_plural = verbose_name
        permissions = {("read_equipmentmanagemodel", u"Can read 仓库管理－设备管理"),
                       ("admin_equipmentmanagemodel", u"Can admin 仓库管理－设备管理")}

class PartsManageModel(models.Model) :
    """
    设备配件管理
    """
    OPERATING_TYPE = (
        ("增加操作", "增加操作"),
        ("入库操作", "入库操作"),
        ("退库操作", "退库操作"),
        ("出库操作", "出库操作"),
        ("盘点操作", "盘点操作"),
    )
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",
                            help_text="操作记录名称(建议唯一)")
    code = models.CharField(max_length=32, name="code",null=True, blank=True,  verbose_name="编码", help_text="操作记录编码(与类型联合唯一)")
    type = models.CharField(max_length=16, choices=OPERATING_TYPE, name="type", verbose_name="类型",
                            help_text="当前操作记录属于的操作记录类型")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="设备配件放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="设备配件放置的仓库名称")
    position_id = models.CharField(max_length=16, name="position_id", verbose_name="仓位id", help_text="产品放置的仓位id")
    position_code = models.CharField(max_length=32, name="position_code", verbose_name="仓位编码", help_text="设备配件放置的仓位编码")
    position_name = models.CharField(max_length=32, name="position_name", verbose_name="仓位名称", help_text="设备配件放置的仓位名称")
    partsType_code = models.CharField(max_length=32, name="partsType_code", verbose_name="设备配件类型编码",
                                         help_text="当前物品的设备配件类型编码")
    partsType_name = models.CharField(max_length=32, name="partsType_name", verbose_name="设备配件类型名称",
                                         help_text="当前物品的设备配件类型名称")
    parts_id = models.CharField(max_length=16, name="parts_id", verbose_name="设备配件id", help_text="当前物品的设备配件id")
    parts_code = models.CharField(max_length=32, name="parts_code", verbose_name="设备配件编码", help_text="当前物品的设备配件编码")
    parts_name = models.CharField(max_length=32, name="parts_name", verbose_name="设备配件名称", help_text="当前物品的设备配件名称")
    handler = models.CharField(max_length=32, name="handler", verbose_name="操作者", help_text="对当前信息进行操作的是谁")
    sum = models.IntegerField(name="sum", verbose_name="操作数量", help_text="当前操作的数量是")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="操作时间", help_text="当前操作的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1",
                                  help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2",
                                  help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3",
                                  help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4",
                                  help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5",
                                  help_text="当前附加属性5")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="文件", help_text="当前操作的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self) :
        return self.code

    class Meta :
        db_table = "PartsManageModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－设备配件管理"
        verbose_name_plural = verbose_name
        permissions = {("read_partsmanagemodel", u"Can read 仓库管理－设备配件管理"),
                       ("admin_partsmanagemodel", u"Can admin 仓库管理－设备配件管理")}


class MaterialManageModel(models.Model):
    """
    物料管理
    """
    OPERATING_TYPE = (
        ("增加操作", "增加操作"),
        ("入库操作", "入库操作"),
        ("退库操作", "退库操作"),
        ("出库操作", "出库操作"),
        ("盘点操作", "盘点操作"),
    )
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",help_text="操作记录名称(建议唯一)")
    code = models.CharField(max_length=32, name="code",null=True, blank=True,  verbose_name="编码", help_text="操作记录编码(与类型联合唯一)")
    type = models.CharField(max_length=16,  choices=OPERATING_TYPE, name="type", verbose_name="类型", help_text="当前操作记录属于的操作记录类型")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="物料放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="物料放置的仓库名称")
    position_id = models.CharField(max_length=16,name="position_id", verbose_name="仓位id", help_text="产品放置的仓位id")
    position_code = models.CharField(max_length=32,name="position_code", verbose_name="仓位编码", help_text="物料放置的仓位编码")
    position_name = models.CharField(max_length=32,name="position_name", verbose_name="仓位名称", help_text="物料放置的仓位名称")
    materialType_code = models.CharField(max_length=32, name="materialType_code", verbose_name="物料类型编码", help_text="当前物品的物料类型编码")
    materialType_name = models.CharField(max_length=32,  name="materialType_name", verbose_name="物料类型名称",help_text="当前物品的物料类型名称")
    material_id = models.CharField(max_length=16, name="material_id", verbose_name="物料id", help_text="当前物品的物料id")
    material_code = models.CharField(max_length=32,name="material_code", verbose_name="物料编码", help_text="当前物品的物料编码")
    material_name = models.CharField(max_length=32, name="material_name", verbose_name="物料名称",help_text="当前物品的物料名称")
    inspectionReportType_code = models.CharField(max_length=32,  null=True, blank=True, name="inspectionReportType_code", verbose_name="质检报告类型编码", help_text="当前物品的质检报告类型编码")
    inspectionReportType_name = models.CharField(max_length=32,   null=True, blank=True, name="inspectionReportType_name", verbose_name="质检报告类型名称",help_text="当前物品的质检报告类型名称")
    inspectionReport_id = models.CharField(max_length=16, null=True, blank=True,  name="inspectionReport_id", verbose_name="质检报告id", help_text="当前物品的质检报告id")
    inspectionReport_code = models.CharField(max_length=32, null=True, blank=True,  name="inspectionReport_code", verbose_name="质检报告编码", help_text="当前物品的质检报告编码")
    inspectionReport_name = models.CharField(max_length=32, null=True, blank=True,   name="inspectionReport_name", verbose_name="质检报告名称",help_text="当前物品的质检报告名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="物料批次", help_text="当前物料的批次")
    handler = models.CharField(max_length=32,name="handler", verbose_name="操作者", help_text="对当前信息进行操作的是谁")
    sum = models.IntegerField( name="sum", verbose_name="操作数量",help_text="当前操作的数量是")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="操作时间", help_text="当前操作的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="文件",help_text="当前操作的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = "MaterialManageModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－物料管理"
        verbose_name_plural = verbose_name
        permissions = {("read_materialmanagemodel", u"Can read 仓库管理－物料管理"),
                       ("admin_materialmanagemodel", u"Can admin 仓库管理－物料管理")}

class SemifinishedManageModel(models.Model):
    """
    半成品管理
    """
    OPERATING_TYPE = (
        ("增加操作", "增加操作"),
        ("入库操作", "入库操作"),
        ("退库操作", "退库操作"),
        ("出库操作", "出库操作"),
        ("盘点操作", "盘点操作"),
    )
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",help_text="操作记录名称(建议唯一)")
    code = models.CharField(max_length=32, name="code",null=True, blank=True,  verbose_name="编码", help_text="操作记录编码(与类型联合唯一)")
    type = models.CharField(max_length=16,  choices=OPERATING_TYPE, name="type", verbose_name="类型", help_text="当前操作记录属于的操作记录类型")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态", help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="物料放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="物料放置的仓库名称")
    position_id = models.CharField(max_length=16,name="position_id", verbose_name="仓位id", help_text="产品放置的仓位id")
    position_code = models.CharField(max_length=32,name="position_code", verbose_name="仓位编码", help_text="物料放置的仓位编码")
    position_name = models.CharField(max_length=32,name="position_name", verbose_name="仓位名称", help_text="物料放置的仓位名称")
    semifinishedType_code = models.CharField(max_length=32, name="semifinishedType_code", verbose_name="半成品类型编码",
                                         help_text="当前物品的半成品类型编码")
    semifinishedType_name = models.CharField(max_length=32, name="semifinishedType_name", verbose_name="半成品类型名称",
                                         help_text="当前物品的半成品类型名称")
    semifinished_id = models.CharField(max_length=16, name="semifinished_id", verbose_name="物料id", help_text="当前物品的物料id")
    semifinished_code = models.CharField(max_length=32,name="semifinished_code", verbose_name="物料编码", help_text="当前物品的物料编码")
    semifinished_name = models.CharField(max_length=32, name="semifinished_name", verbose_name="物料名称",help_text="当前物品的物料名称")
    inspectionReportType_code = models.CharField(max_length=32,  null=True, blank=True, name="inspectionReportType_code", verbose_name="质检报告类型编码", help_text="当前物品的质检报告类型编码")
    inspectionReportType_name = models.CharField(max_length=32,   null=True, blank=True, name="inspectionReportType_name", verbose_name="质检报告类型名称",help_text="当前物品的质检报告类型名称")
    inspectionReport_id = models.CharField(max_length=16, null=True, blank=True,  name="inspectionReport_id", verbose_name="质检报告id", help_text="当前物品的质检报告id")
    inspectionReport_code = models.CharField(max_length=32, null=True, blank=True,  name="inspectionReport_code", verbose_name="质检报告编码", help_text="当前物品的质检报告编码")
    inspectionReport_name = models.CharField(max_length=32, null=True, blank=True,   name="inspectionReport_name", verbose_name="质检报告名称",help_text="当前物品的质检报告名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="物料批次", help_text="当前物料的批次")
    handler = models.CharField(max_length=32,name="handler", verbose_name="操作者", help_text="对当前信息进行操作的是谁")
    sum = models.IntegerField( name="sum", verbose_name="操作数量",help_text="当前操作的数量是")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="操作时间", help_text="当前操作的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="文件",help_text="当前操作的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")
    def __str__(self):
        return self.code

    class Meta:
        db_table = "SemifinishedManageModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－半成品管理"
        verbose_name_plural = verbose_name
        permissions = {("read_semifinishedmanagemodel", u"Can read 仓库管理－半成品管理"),
                       ("admin_semifinishedmanagemodel", u"Can admin 仓库管理－半成品管理")}

class ProductManageModel(models.Model):
    """
    产品管理
    """
    OPERATING_TYPE = (
        ("增加操作", "增加操作"),
        ("入库操作", "入库操作"),
        ("退库操作", "退库操作"),
        ("出库操作", "出库操作"),
        ("盘点操作", "盘点操作"),
    )
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("完成", "完成"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name", null=True, blank=True, verbose_name="名称",help_text="操作记录名称(建议唯一)")
    code = models.CharField(max_length=32, name="code",null=True, blank=True,  verbose_name="编码", help_text="操作记录编码(与类型联合唯一)")
    type = models.CharField(max_length=16,  choices=OPERATING_TYPE, name="type", verbose_name="类型", help_text="当前操作记录属于的操作记录类型")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state",verbose_name="状态", help_text="当前信息的状态")
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码", help_text="物料放置的仓库编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称", help_text="物料放置的仓库名称")
    position_id = models.CharField(max_length=16,name="position_id", verbose_name="仓位id", help_text="产品放置的仓位id")
    position_code = models.CharField(max_length=32,name="position_code", verbose_name="仓位编码", help_text="物料放置的仓位编码")
    position_name = models.CharField(max_length=32,name="position_name", verbose_name="仓位名称", help_text="物料放置的仓位名称")
    productType_code = models.CharField(max_length=32, name="productType_code", verbose_name="产品类型编码", help_text="当前物品的产品类型编码")
    productType_name = models.CharField(max_length=32, name="productType_name", verbose_name="产品类型名称",help_text="当前物品的产品类型名称")
    product_id = models.CharField(max_length=16, name="product_id", verbose_name="产品id", help_text="当前物品的产品id")
    product_code = models.CharField(max_length=32, name="product_code", verbose_name="产品编码", help_text="当前物品的产品编码")
    product_name = models.CharField(max_length=32, name="product_name", verbose_name="产品名称", help_text="当前物品的产品名称")
    inspectionReportType_code = models.CharField(max_length=32,  null=True, blank=True, name="inspectionReportType_code", verbose_name="质检报告类型编码", help_text="当前物品的质检报告类型编码")
    inspectionReportType_name = models.CharField(max_length=32,   null=True, blank=True, name="inspectionReportType_name", verbose_name="质检报告类型名称",help_text="当前物品的质检报告类型名称")
    inspectionReport_id = models.CharField(max_length=16, null=True, blank=True,  name="inspectionReport_id", verbose_name="质检报告id", help_text="当前物品的质检报告id")
    inspectionReport_code = models.CharField(max_length=32, null=True, blank=True,  name="inspectionReport_code", verbose_name="质检报告编码", help_text="当前物品的质检报告编码")
    inspectionReport_name = models.CharField(max_length=32, null=True, blank=True,   name="inspectionReport_name", verbose_name="质检报告名称",help_text="当前物品的质检报告名称")
    batch = models.CharField(max_length=32,null=True, blank=True, name="batch", verbose_name="产品批次", help_text="当前产品的批次")
    handler = models.CharField(max_length=32,name="handler", verbose_name="操作者", help_text="对当前信息进行操作的是谁")
    sum = models.IntegerField( name="sum", verbose_name="操作数量",help_text="当前操作的数量是")
    dataTime = models.DateTimeField(name="dataTime", null=True, blank=True,verbose_name="操作时间", help_text="当前操作的时间")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="文件", help_text="当前操作的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ProductManageModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－产品管理"
        verbose_name_plural = verbose_name
        permissions = {("read_productmanagemodel", u"Can read 仓库管理－产品管理"),
                       ("admin_productmanagemodel", u"Can admin 仓库管理－产品管理")}
        

class MaterialWaringRuleItemModel(models.Model):
    """
    物料库存预警规则子项
    """
    id = models.AutoField(primary_key=True, unique=True)
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码",
                                      help_text="当前规则下指定仓库的编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称",
                                      help_text="当前规则下指定仓库的名称")
    materialType_code = models.CharField(max_length=32, name="materialType_code", verbose_name="物料类型编码", help_text="当前物品的物料类型编码")
    materialType_name = models.CharField(max_length=32,  name="materialType_name", verbose_name="物料类型名称",help_text="当前物品的物料类型名称")
    material_id = models.CharField(max_length=16, name="material_id", verbose_name="物料id", help_text="当前物品的物料id")
    material_code = models.CharField(max_length=32, name="material_code", verbose_name="物料编码", help_text="当前物品的物料编码")
    material_name = models.CharField(max_length=32,  name="material_name", verbose_name="物料名称",help_text="当前物品的物料名称")
    batch = models.CharField(max_length=32, null=True, blank=True, name="batch", verbose_name="产品批次",
                             help_text="当前规则下指定物料的批次")
    minimum = models.FloatField(null=True, blank=True, name="minimum", verbose_name="最少量",
                               help_text="当前物料最小库存限值")
    maximum = models.FloatField(null=True, blank=True, name="maximum", verbose_name="最大量",
                               help_text="当前物料最大库存限值")
    lowthreshold = models.FloatField(null=True, blank=True, name="lowthreshold", verbose_name="低阀值",
                                    help_text="当前物料低阀值预警")
    highthreshold = models.FloatField(null=True, blank=True, name="highthreshold", verbose_name="高阀值",
                                     help_text="当前物料高阀值预警")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'MaterialWaringRuleItemModel'
        app_label = "warehouse"
        verbose_name = "仓库管理－物料库存预警规则子项"
        verbose_name_plural = verbose_name


class MaterialWaringRuleModel(models.Model):
    """
    物料库存预警规则
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="预警规则名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="物料预警规则编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    child = models.ManyToManyField(MaterialWaringRuleItemModel, blank=True, verbose_name="包含子项",
                                       help_text="当前物料预警规则包含的子项")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="产品预警规则文件",
                                  help_text="物料预警规则的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "MaterialWaringRuleModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－物料库存预警规则"
        verbose_name_plural = verbose_name
        permissions = {("read_materialwaringrulemodel", u"Can read 仓库管理－物料库存预警规则"),
                       ("admin_materialwaringrulemodel", u"Can admin 仓库管理－物料库存预警规则")}


class SemifinishedWaringRuleItemModel(models.Model):
    """
    半成品库存预警规则子项
    """
    id = models.AutoField(primary_key=True, unique=True)
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码",
                                      help_text="当前规则下指定仓库的编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称",
                                      help_text="当前规则下指定仓库的名称")
    semifinishedType_code = models.CharField(max_length=32, name="semifinishedType_code", verbose_name="半成品类型编码", help_text="当前物品的半成品类型编码")
    semifinishedType_name = models.CharField(max_length=32,  name="semifinishedType_name", verbose_name="半成品类型名称",help_text="当前物品的半成品类型名称")
    semifinished_id = models.CharField(max_length=16, name="semifinished_id", verbose_name="半成品id", help_text="当前物品的半成品id")
    semifinished_code = models.CharField(max_length=32, name="semifinished_code", verbose_name="半成品编码", help_text="当前物品的半成品编码")
    semifinished_name = models.CharField(max_length=32,  name="semifinished_name", verbose_name="半成品名称",help_text="当前物品的半成品名称")
    batch = models.CharField(max_length=32, null=True, blank=True, name="batch", verbose_name="产品批次",
                             help_text="当前规则下指定半成品的批次")
    minimum = models.FloatField(null=True, blank=True, name="minimum", verbose_name="最少量",
                               help_text="当前半成品最小库存限值")
    maximum = models.FloatField(null=True, blank=True, name="maximum", verbose_name="最大量",
                               help_text="当前半成品最大库存限值")
    lowthreshold = models.FloatField(null=True, blank=True, name="lowthreshold", verbose_name="低阀值",
                                    help_text="当前半成品低阀值预警")
    highthreshold = models.FloatField(null=True, blank=True, name="highthreshold", verbose_name="高阀值",
                                     help_text="当前半成品高阀值预警")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'SemifinishedWaringRuleItemModel'
        app_label = "warehouse"
        verbose_name = "仓库管理－半成品库存预警规则子项"
        verbose_name_plural = verbose_name


class SemifinishedWaringRuleModel(models.Model):
    """
    半成品库存预警规则
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="预警规则名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="半成品预警规则编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    child = models.ManyToManyField(SemifinishedWaringRuleItemModel, blank=True, verbose_name="包含子项",
                                       help_text="当前半成品预警规则包含的子项")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="产品预警规则文件",
                                  help_text="半成品预警规则的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "SemifinishedWaringRuleModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－半成品库存预警规则"
        verbose_name_plural = verbose_name
        permissions = {("read_semifinishedwaringrulemodel", u"Can read 仓库管理－半成品库存预警规则"),
                       ("admin_semifinishedwaringrulemodel", u"Can admin 仓库管理－半成品库存预警规则")}

class ProductWaringRuleItemModel(models.Model):
    """
    产品库存预警规则子项
    """
    id = models.AutoField(primary_key=True, unique=True)
    warehouse_code = models.CharField(max_length=32, name="warehouse_code", verbose_name="仓库编码",
                                      help_text="当前规则下指定仓库的编码")
    warehouse_name = models.CharField(max_length=32, name="warehouse_name", verbose_name="仓库名称",
                                      help_text="当前规则下指定仓库的名称")
    productType_code = models.CharField(max_length=32, name="productType_code", verbose_name="产品类型编码", help_text="当前物品的产品类型编码")
    productType_name = models.CharField(max_length=32,  name="productType_name", verbose_name="产品类型名称",help_text="当前物品的产品类型名称")
    product_id = models.CharField(max_length=16, name="product_id", verbose_name="产品id", help_text="当前物品的产品id")
    product_code = models.CharField(max_length=32, name="product_code", verbose_name="产品编码", help_text="当前物品的产品编码")
    product_name = models.CharField(max_length=32,  name="product_name", verbose_name="产品名称",help_text="当前物品的产品名称")
    batch = models.CharField(max_length=32, null=True, blank=True, name="batch", verbose_name="产品批次",
                             help_text="当前规则下指定产品的批次")
    minimum = models.FloatField(null=True, blank=True, name="minimum", verbose_name="最少量",
                               help_text="当前产品最小库存限值")
    maximum = models.FloatField( null=True, blank=True, name="maximum", verbose_name="最大量",
                               help_text="当前产品最大库存限值")
    lowthreshold = models.FloatField(null=True, blank=True, name="lowthreshold", verbose_name="低阀值",
                                    help_text="当前产品低阀值预警")
    highthreshold = models.FloatField(null=True, blank=True, name="highthreshold", verbose_name="高阀值",
                                     help_text="当前产品高阀值预警")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")

    def __str__(self):
        return str(self.id)

    class Meta:
        db_table = 'ProductWaringRuleItemModel'
        app_label = "warehouse"
        verbose_name = "仓库管理－产品库存预警规则子项"
        verbose_name_plural = verbose_name


class ProductWaringRuleModel(models.Model):
    """
    产品库存预警规则
    """
    STATUS = (
        ("新建", "新建"),
        ("审核中", "审核中"),
        ("使用中", "使用中"),
        ("作废", "作废"),
    )
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=32, name="name",null=True, blank=True, verbose_name="名称", help_text="预警规则名称(建议唯一)")
    code = models.CharField(max_length=32, unique=True, name="code", verbose_name="编码", help_text="产品预警规则编码(必须唯一)")
    state = models.CharField(max_length=16, choices=STATUS, default="新建", name="state", verbose_name="状态",
                             help_text="当前信息的状态")
    child = models.ManyToManyField(ProductWaringRuleItemModel, blank=True, verbose_name="包含子项",
                                       help_text="当前产品预警规则包含的子项")
    attribute1 = models.CharField(max_length=32, null=True, blank=True, name="attribute1", verbose_name="属性1", help_text="当前附加属性1")
    attribute2 = models.CharField(max_length=32, null=True, blank=True, name="attribute2", verbose_name="属性2", help_text="当前附加属性2")
    attribute3 = models.CharField(max_length=32, null=True, blank=True, name="attribute3", verbose_name="属性3", help_text="当前附加属性3")
    attribute4 = models.CharField(max_length=32, null=True, blank=True, name="attribute4", verbose_name="属性4", help_text="当前附加属性4")
    attribute5 = models.CharField(max_length=32, null=True, blank=True, name="attribute5", verbose_name="属性5", help_text="当前附加属性5")
    file = models.ManyToManyField(WarehouseFileModel, blank=True, name="file", verbose_name="产品预警规则文件",
                                  help_text="产品预警规则的文件信息")
    desc = models.TextField(null=True, blank=True, name="desc", verbose_name="备注",
                            help_text="当前信息未列出的字段项，可以在此字段描述.每一项用;隔开")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间", help_text="当前信息创建的时间,后台会自动填充此字段")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间", help_text="当前信息最后的更新时间,后台会自动填充此字段")
    create_user = models.CharField(max_length=32, name="create_user", verbose_name="创建账号", help_text="创建当前信息的账号名称")
    auditor = models.CharField(max_length=32, name="auditor", verbose_name="审核账号", help_text="可对当前信息进行审核的账号名称")
    alter = models.ManyToManyField(WarehouseAlterRecordModel, blank=True, name="alter", verbose_name="审核记录",
                                   help_text="当前信息的审核记录")

    def __str__(self):
        return self.code

    class Meta:
        db_table = "ProductWaringRuleModel"
        app_label = 'warehouse'
        verbose_name = "仓库管理－产品库存预警规则"
        verbose_name_plural = verbose_name
        permissions = {("read_productwaringrulemodel", u"Can read 仓库管理－产品库存预警规则"),
                       ("admin_productwaringrulemodel", u"Can admin 仓库管理－产品库存预警规则")}