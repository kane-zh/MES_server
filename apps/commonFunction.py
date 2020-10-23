from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden,HttpResponse
from user.models import UserAuditRecordModel
from apps.process.models.basicinfor_model import ProcessAuditRecordModel
from apps.warehouse.models.basicinfor_model import WarehouseAuditRecordModel
from apps.quality.models.basicinfor_model import QualityAuditRecordModel
from apps.equipment.models.basicinfor_model import EquipmentAuditRecordModel
from apps.plan.models.basicinfor_model import PlanAuditRecordModel
from apps.production.models.basicinfor_model import ProductionAuditRecordModel
from apps.lean.models.basicinfor_model import LeanAuditRecordModel
import datetime
import requests
import json
import uuid
def validate_states(curstate, newstate):
    """
 　　类型信息，基本信息
    """
    if (curstate == "新建" and \
            (newstate == "审核中" or newstate == "作废")):
        return newstate
    if (curstate == "审核中" and \
         ( newstate == "使用中" or newstate == "新建" or newstate == "作废")):
        return newstate
    if (curstate == "使用中" and \
            ( newstate == "作废")):
        return newstate
    raise serializers.ValidationError("不能从" + curstate + "更新到" + newstate)
    return newstate

def validate_states1(curstate, newstate):
    """
　　　记录信息
    """
    if (curstate == "新建" and \
            (newstate == "审核中" or newstate == "作废")):
        return newstate
    if (curstate == "审核中" and \
         ( newstate == "完成" or newstate == "新建" or newstate == "作废")):
        return newstate
    if (curstate == "完成" and \
            ( newstate == "作废")):
        return newstate
    raise serializers.ValidationError("不能从" + curstate + "更新到" + newstate)
    return newstate

def validate_states2(curstate, newstate):
    """
     销售订单状态
    """
    if (curstate == "新建" and \
            (newstate == "审核中" or newstate == "作废")):
        return newstate
    if (curstate == "审核中" and \
        (newstate == "使用中" or newstate == "新建" or newstate == "作废")):
        return newstate
    if (curstate == "使用中" and  (newstate == "终止")):
        return newstate
    if (curstate == "完成" and  (newstate == "作废")):
        return newstate
    if (curstate == "终止" and  (newstate == "作废")):
        return newstate
    raise serializers.ValidationError("不能从" + curstate + "更新到" + newstate)
    return newstate

def validate_states3(curstate, newstate):
    """
　　　生产任务，管理计划
    """

    if (curstate == "新建" and \
            (newstate == "审核中" or newstate == "作废")):
        return newstate
    if (curstate == "审核中" and \
        (newstate == "使用中" or newstate == "新建" or newstate == "作废")):
        return newstate
    if (curstate == "使用中" and  (newstate == "终止" or newstate == "挂起")):
        return newstate
    if (curstate == "挂起" and  (newstate == "终止" or newstate == "使用中")):
        return newstate
    if (curstate == "完成" and  (newstate == "作废")):
        return newstate
    if (curstate == "终止" and  (newstate == "作废")):
        return newstate
    raise serializers.ValidationError("不能从" + curstate + "更新到" + newstate)
    return newstate


def validate_states4(curstate, newstate):
    """
 　　采购计划，维护计划
    """
    if (curstate == "新建" and \
            (newstate == "审核中" or newstate == "作废")):
        return newstate
    if (curstate == "审核中" and \
        (newstate == "使用中" or newstate == "新建" or newstate == "作废")):
        return newstate
    if (curstate == "使用中" and  (newstate == "终止"  or newstate == "完成")):
        return newstate
    if (curstate == "完成" and  (newstate == "作废")):
        return newstate
    if (curstate == "终止" and  (newstate == "作废")):
        return newstate
    raise serializers.ValidationError("不能从" + curstate + "更新到" + newstate)
    return newstate

class StandardResultsSetPagination (PageNumberPagination):
    """
    通用分页器类
    """
    page_size = 20
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 9999


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    通用权限验证类
    验证当前用户与信息创建用户是否一致
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.create_user == request.user

class viewMiddleException(Exception):
    """
     视图层拦截异常
    """
    def __init__(self, error):
        self.error = error,
        self.name='viewMiddleException',
        self.cod=403


class RecordEventMiddleWare(MiddlewareMixin):
    """
    全局数据请求/响应中间件,用于保存用户操作
    """
    # 这个方法的调用时机在 Django 接收到 request 之后，但仍未解析URL以确定应当运行的 view 之前
    def process_request(self, request):
        if request.path== '/login' :
            node = uuid.getnode()
            mac = uuid.UUID(int=node).hex[-12 :]
            url = 'http://124.70.176.250:8000/user/ServerInfor/?mac='+mac # 改路由
            headers = {'content-type' : "application/json"}
            try:
                response = requests.get(url, headers=headers,timeout=3)
                response = json.loads(response.text)
            except Exception as e:
                return None
            if response :
                data=response[0]
                if data['enable']==False:
                    return  HttpResponse(status=502,content=data['message'])
            else:
                url = 'http://49.4.115.187:8000/user/ServerInfor/'  # 改路由
                values = {
                    "mac" : mac,
                }
                try :
                   response = requests.post(url, data=json.dumps(values), headers=headers,timeout=3)
                except Exception as e:
                   return None
        return None

    # 这个方法的调用时机在 Django 执行完 request 预处理函数并确定待执行的 view 之后，但在 view 函数实际执行之前
    def process_view(self, request, callback, callback_args, callback_kwargs):
        return None

    # 这个方法的调用时机在 Django执行view函数并生成 response 之后
    def process_response(self, request, response):

        path_model = {"user": UserAuditRecordModel,
                      "process": ProcessAuditRecordModel,
                      "warehouse": WarehouseAuditRecordModel,
                      "quality": QualityAuditRecordModel,
                      "equipment": EquipmentAuditRecordModel,
                      "plan": PlanAuditRecordModel,
                      "production": ProductionAuditRecordModel,
                      "lean": LeanAuditRecordModel
                     }
        url = request.path.split('/')
        if url[1] in path_model.keys():
            if request.method == "POST" :
                if hasattr(response, 'data'):
                    responseData = response.data
                    if 'id' in response.data :
                       id=response.data['id']
                    else:
                       id=""
                else:
                    responseData=''
                    id=""
                path_model[(url[1])].objects.create(
                    uri=url[2],
                    uri_id=id,
                    classes="POST",
                    user=request.user,
                    result=response.status_code,
                    content=responseData)
            if request.method == "PUT":
                if hasattr(response, 'data') :
                    responseData = response.data
                else :
                    responseData = ''
                path_model[(url[1])].objects.create(
                    uri=url[2],
                    uri_id=url[3],
                    classes="PUT",
                    user=request.user,
                    result=response.status_code,
                    content=responseData)
            if request.method == "PATCH" :
                if hasattr(response, 'data') :
                    responseData = response.data
                else :
                    responseData = ''
                path_model[(url[1])].objects.create(
                    uri=url[2],
                    uri_id=url[3],
                    classes="PATCH" ,
                    user=request.user,
                    result=response.status_code,
                    content=responseData)
            if request.method == "DELETE":
                path_model[(url[1])].objects.create(
                    uri=url[2],
                    uri_id=url[3],
                    classes="DELETE",
                    user=request.user,
                    result=response.status_code,
                    content="")
        return response

    #   这个方法只有在request处理过程中出了问题并且 view函数抛出了一个未捕获的异常时才会被调用
    def process_exception(self, request, exception):
        if exception.__class__.__name__ is 'viewMiddleException':
          return  HttpResponseForbidden(exception.error )
        return None
