from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
import shutil
# -*- coding:utf-8 -*-
extensions = [
    # 账号管理模块
    Extension(
        "apps.user.filters.basicinfor_filters",
        ["apps/user/filters/basicinfor_filters.py"]
    ),
    Extension(
        "apps.user.models",
        ["apps/user/models.py"]
    ),
    Extension(
        "apps.user.serializes.basicinfor_serialize",
        ["apps/user/serializes/basicinfor_serialize.py"]
    ),
    Extension(
        "apps.user.views.basicinfor_view",
        ["apps/user/views/basicinfor_view.py"]
    ),
    Extension(
        "apps.user.admin",
        ["apps/user/admin.py"]
    ),
    Extension(
        "apps.user.apps",
        ["apps/user/apps.py"]
    ),
    Extension(
        "apps.user.tests",
        ["apps/user/tests.py"]
    ),
    Extension(
        "apps.user.urls",
        ["apps/user/urls.py"]
    ),
    # 设备管理模块
    Extension(
        "apps.equipment.filters.basicinfor_filters",
        ["apps/equipment/filters/basicinfor_filters.py"]
    ),
    Extension(
        "apps.equipment.filters.recording_filters",
        ["apps/equipment/filters/recording_filters.py"]
    ),
    Extension(
        "apps.equipment.models.basicinfor_model",
        ["apps/equipment/models/basicinfor_model.py"]
    ),
    Extension(
        "apps.equipment.models.recording_model",
        ["apps/equipment/models/recording_model.py"]
    ),
    Extension(
        "apps.equipment.serializes.basicinfor_serialize",
        ["apps/equipment/serializes/basicinfor_serialize.py"]
    ),
    Extension(
        "apps.equipment.serializes.recording_serialize",
        ["apps/equipment/serializes/recording_serialize.py"]
    ),
    Extension(
        "apps.equipment.views.basicinfor_view",
        ["apps/equipment/views/basicinfor_view.py"]
    ),
    Extension(
        "apps.equipment.views.recording_view",
        ["apps/equipment/views/recording_view.py"]
    ),
    Extension(
        "apps.equipment.admin",
        ["apps/equipment/admin.py"]
    ),
    Extension(
        "apps.equipment.apps",
        ["apps/equipment/apps.py"]
    ),
    Extension(
        "apps.equipment.tests",
        ["apps/equipment/tests.py"]
    ),
    Extension(
        "apps.equipment.urls",
        ["apps/equipment/urls.py"]
    ),

    # 精益管理模块
    Extension(
        "apps.lean.filters.basicinfor_filters",
        ["apps/lean/filters/basicinfor_filters.py"]
    ),
    Extension(
        "apps.lean.models.basicinfor_model",
        ["apps/lean/models/basicinfor_model.py"]
    ),
    Extension(
        "apps.lean.serializes.basicinfor_serialize",
        ["apps/lean/serializes/basicinfor_serialize.py"]
    ),
    Extension(
        "apps.lean.views.basicinfor_view",
        ["apps/lean/views/basicinfor_view.py"]
    ),
    Extension(
        "apps.lean.admin",
        ["apps/lean/admin.py"]
    ),
    Extension(
        "apps.lean.apps",
        ["apps/lean/apps.py"]
    ),
    Extension(
        "apps.lean.tests",
        ["apps/lean/tests.py"]
    ),
    Extension(
        "apps.lean.urls",
        ["apps/lean/urls.py"]
    ),

    # 计划管理模块
    Extension(
        "apps.plan.filters.basicinfor_filters",
        ["apps/plan/filters/basicinfor_filters.py"]
    ),
    Extension(
        "apps.plan.models.basicinfor_model",
        ["apps/plan/models/basicinfor_model.py"]
    ),
    Extension(
        "apps.plan.serializes.basicinfor_serialize",
        ["apps/plan/serializes/basicinfor_serialize.py"]
    ),
    Extension(
        "apps.plan.views.basicinfor_view",
        ["apps/plan/views/basicinfor_view.py"]
    ),
    Extension(
        "apps.plan.admin",
        ["apps/plan/admin.py"]
    ),
    Extension(
        "apps.plan.apps",
        ["apps/plan/apps.py"]
    ),
    Extension(
        "apps.plan.tests",
        ["apps/plan/tests.py"]
    ),
    Extension(
        "apps.plan.urls",
        ["apps/plan/urls.py"]
    ),

    # 工艺管理模块
    Extension(
        "apps.process.filters.basicinfor_filters",
        ["apps/process/filters/basicinfor_filters.py"]
    ),
    Extension(
        "apps.process.models.basicinfor_model",
        ["apps/process/models/basicinfor_model.py"]
    ),
    Extension(
        "apps.process.serializes.basicinfor_serialize",
        ["apps/process/serializes/basicinfor_serialize.py"]
    ),
    Extension(
        "apps.process.views.basicinfor_view",
        ["apps/process/views/basicinfor_view.py"]
    ),
    Extension(
        "apps.process.admin",
        ["apps/process/admin.py"]
    ),
    Extension(
        "apps.process.apps",
        ["apps/process/apps.py"]
    ),
    Extension(
        "apps.process.tests",
        ["apps/process/tests.py"]
    ),
    Extension(
        "apps.process.urls",
        ["apps/process/urls.py"]
    ),

    # 生产管理模块
    Extension(
        "apps.production.filters.basicinfor_filters",
        ["apps/production/filters/basicinfor_filters.py"]
    ),
    Extension(
        "apps.production.filters.recording_filters",
        ["apps/production/filters/recording_filters.py"]
    ),
    Extension(
        "apps.production.models.basicinfor_model",
        ["apps/production/models/basicinfor_model.py"]
    ),
    Extension(
        "apps.production.models.recording_model",
        ["apps/production/models/recording_model.py"]
    ),
    Extension(
        "apps.production.serializes.basicinfor_serialize",
        ["apps/production/serializes/basicinfor_serialize.py"]
    ),
    Extension(
        "apps.production.serializes.recording_serialize",
        ["apps/production/serializes/recording_serialize.py"]
    ),
    Extension(
        "apps.production.views.basicinfor_view",
        ["apps/production/views/basicinfor_view.py"]
    ),
    Extension(
        "apps.production.views.recording_view",
        ["apps/production/views/recording_view.py"]
    ),
    Extension(
        "apps.production.admin",
        ["apps/production/admin.py"]
    ),
    Extension(
        "apps.production.apps",
        ["apps/production/apps.py"]
    ),
    Extension(
        "apps.production.tests",
        ["apps/production/tests.py"]
    ),
    Extension(
        "apps.production.urls",
        ["apps/production/urls.py"]
    ),

    # 品质管理模块
    Extension(
        "apps.quality.filters.basicinfor_filters",
        ["apps/quality/filters/basicinfor_filters.py"]
    ),
    Extension(
        "apps.quality.filters.recording_filters",
        ["apps/quality/filters/recording_filters.py"]
    ),
    Extension(
        "apps.quality.models.basicinfor_model",
        ["apps/quality/models/basicinfor_model.py"]
    ),
    Extension(
        "apps.quality.models.recording_model",
        ["apps/quality/models/recording_model.py"]
    ),
    Extension(
        "apps.quality.serializes.basicinfor_serialize",
        ["apps/quality/serializes/basicinfor_serialize.py"]
    ),
    Extension(
        "apps.quality.serializes.recording_serialize",
        ["apps/quality/serializes/recording_serialize.py"]
    ),
    Extension(
        "apps.quality.views.basicinfor_view",
        ["apps/quality/views/basicinfor_view.py"]
    ),
    Extension(
        "apps.quality.views.recording_view",
        ["apps/quality/views/recording_view.py"]
    ),
    Extension(
        "apps.quality.admin",
        ["apps/quality/admin.py"]
    ),
    Extension(
        "apps.quality.apps",
        ["apps/quality/apps.py"]
    ),
    Extension(
        "apps.quality.tests",
        ["apps/quality/tests.py"]
    ),
    Extension(
        "apps.quality.urls",
        ["apps/quality/urls.py"]
    ),

    # 仓库管理模块
    Extension(
        "apps.warehouse.filters.basicinfor_filters",
        ["apps/warehouse/filters/basicinfor_filters.py"]
    ),
    Extension(
        "apps.warehouse.filters.inventory_filters",
        ["apps/warehouse/filters/inventory_filters.py"]
    ),
    Extension(
        "apps.warehouse.models.basicinfor_model",
        ["apps/warehouse/models/basicinfor_model.py"]
    ),
    Extension(
        "apps.warehouse.models.inventory_model",
        ["apps/warehouse/models/inventory_model.py"]
    ),
    Extension(
        "apps.warehouse.serializes.basicinfor_serialize",
        ["apps/warehouse/serializes/basicinfor_serialize.py"]
    ),
    Extension(
        "apps.warehouse.serializes.inventory_serialize",
        ["apps/warehouse/serializes/inventory_serialize.py"]
    ),
    Extension(
        "apps.warehouse.views.basicinfor_view",
        ["apps/warehouse/views/basicinfor_view.py"]
    ),
    Extension(
        "apps.warehouse.views.inventory_view",
        ["apps/warehouse/views/inventory_view.py"]
    ),
    Extension(
        "apps.warehouse.admin",
        ["apps/warehouse/admin.py"]
    ),
    Extension(
        "apps.warehouse.apps",
        ["apps/warehouse/apps.py"]
    ),
    Extension(
        "apps.warehouse.tests",
        ["apps/warehouse/tests.py"]
    ),
    Extension(
        "apps.warehouse.urls",
        ["apps/warehouse/urls.py"]
    ),

    # 公共模块
    Extension(
        "apps.commonFunction",
        ["apps/commonFunction.py"]
    ),

]
files = [
    # 账号管理模块
    "apps/user/filters/basicinfor_filters",
    "apps/user/models",
    "apps/user/serializes/basicinfor_serialize",
    "apps/user/views/basicinfor_view",
    "apps/user/admin",
    "apps/user/apps",
    "apps/user/tests",
    "apps/user/urls",
    # 设备管理模块
    "apps/equipment/filters/basicinfor_filters",
    "apps/equipment/filters/recording_filters",
    "apps/equipment/models/basicinfor_model",
    "apps/equipment/models/recording_model",
    "apps/equipment/serializes/basicinfor_serialize",
    "apps/equipment/serializes/recording_serialize",
    "apps/equipment/views/basicinfor_view",
    "apps/equipment/views/recording_view",
    "apps/equipment/admin",
    "apps/equipment/apps",
    "apps/equipment/tests",
    "apps/equipment/urls",
    # 精益管理模块
    "apps/lean/filters/basicinfor_filters",
    "apps/lean/models/basicinfor_model",
    "apps/lean/serializes/basicinfor_serialize",
    "apps/lean/views/basicinfor_view",
    "apps/lean/admin",
    "apps/lean/apps",
    "apps/lean/tests",
    "apps/lean/urls",
    # 计划管理模块
    "apps/plan/filters/basicinfor_filters",
    "apps/plan/models/basicinfor_model",
    "apps/plan/serializes/basicinfor_serialize",
    "apps/plan/views/basicinfor_view",
    "apps/plan/admin",
    "apps/plan/apps",
    "apps/plan/tests",
    "apps/plan/urls",
    # 工艺管理模块
    "apps/process/filters/basicinfor_filters",
    "apps/process/models/basicinfor_model",
    "apps/process/serializes/basicinfor_serialize",
    "apps/process/views/basicinfor_view",
    "apps/process/admin",
    "apps/process/apps",
    "apps/process/tests",
    "apps/process/urls",
    # 生产管理模块
    "apps/production/filters/basicinfor_filters",
    "apps/production/filters/recording_filters",
    "apps/production/models/basicinfor_model",
    "apps/production/models/recording_model",
    "apps/production/serializes/basicinfor_serialize",
    "apps/production/serializes/recording_serialize",
    "apps/production/views/basicinfor_view",
    "apps/production/views/recording_view",
    "apps/production/admin",
    "apps/production/apps",
    "apps/production/tests",
    "apps/production/urls",
    # 品质管理模块
    "apps/quality/filters/basicinfor_filters",
    "apps/quality/filters/recording_filters",
    "apps/quality/models/basicinfor_model",
    "apps/quality/models/recording_model",
    "apps/quality/serializes/basicinfor_serialize",
    "apps/quality/serializes/recording_serialize",
    "apps/quality/views/basicinfor_view",
    "apps/quality/views/recording_view",
    "apps/quality/admin",
    "apps/quality/apps",
    "apps/quality/tests",
    "apps/quality/urls",
    # 仓库管理模块
    "apps/warehouse/filters/basicinfor_filters",
    "apps/warehouse/filters/inventory_filters",
    "apps/warehouse/models/basicinfor_model",
    "apps/warehouse/models/inventory_model",
    "apps/warehouse/serializes/basicinfor_serialize",
    "apps/warehouse/serializes/inventory_serialize",
    "apps/warehouse/views/basicinfor_view",
    "apps/warehouse/views/inventory_view",
    "apps/warehouse/admin",
    "apps/warehouse/apps",
    "apps/warehouse/tests",
    "apps/warehouse/urls",

    # 公共模块
    "apps/commonFunction"
]


setup(
    name = "mes_server",
    cmdclass = {'build_ext': build_ext},
    ext_modules=cythonize(extensions),
)

## 批量删除文件或文件夹
for path in files:
     os.remove(path + ".py")
     os.remove(path + ".c")
shutil.rmtree("build")
shutil.rmtree("venv")
shutil.rmtree(".git")

