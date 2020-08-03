"""Mes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    rtyhyguhkij. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    rtyhyguhkij. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    rtyhyguhkij. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include ,url
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token
from Mes.settings import MEDIA_ROOT
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    path('api-auth/', include('rest_framework.urls')),  # 用户登录模块
    path('doc/', include_docs_urls(title='API文档')),
    path('login', obtain_jwt_token),   # 获取用户jwt
    path('user/', include('apps.user.urls')),  # 用户管理模块
    path('process/', include('apps.process.urls')),  # 工艺管理模块
    path('quality/', include('apps.quality.urls')),  # 品质管理模块
    path('plan/', include('apps.plan.urls')),  # 计划管理模块
    path('warehouse/', include('apps.warehouse.urls')),  # 仓库管理模块
    path('production/', include('apps.production.urls')),  # 生产管理模块
    path('equipment/', include('apps.equipment.urls')),  # 设备管理模块
    path('lean/', include('apps.lean.urls')),  # 精益管理模块
]
