from django.conf.urls import  include
from django.urls import  path
from rest_framework.routers import DefaultRouter
from apps.lean.views.basicinfor_view import *


router = DefaultRouter()
router.register('auditRecord', LeanAuditRecordView, basename="LeanAuditRecordView")
router.register('alterRecord', LeanAlterRecordView, basename="LeanAlterRecordView")
router.register('image', LeanImageView, basename="LeanImageView")
router.register('file', LeanFileView, basename="LeanFileView")
router.register('board', LeanBoardView, basename="LeanBoardView")

urlpatterns = [
    path(r'', include(router.urls)),
]
