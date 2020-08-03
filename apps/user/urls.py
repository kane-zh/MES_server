from django.conf.urls import  include
from django.urls import  path
from rest_framework.routers import DefaultRouter
from apps.user.views.basicinfor_view import *

router = DefaultRouter()
router.register('auditRecord', UserAuditRecordView, basename="UserAuditRecordView")
router.register('permissionInfor', PermissionInforView, basename="PermissionInforView")
router.register('groupInfor', GroupInforView, basename="GroupInforView")
router.register('userInfor', UserInforView, basename="UserInforView")
urlpatterns = [
    path(r'', include(router.urls))
]
