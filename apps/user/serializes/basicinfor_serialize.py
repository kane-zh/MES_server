from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group ,Permission
from user.models import *
from Mes import settings
User= get_user_model()

# region  操作日志 序列化器

class UserAuditRecordSerialize_List(serializers.ModelSerializer):
    """
    操作日志---list
    """

    class Meta:
        model = UserAuditRecordModel
        fields = ("id", "uri", "uri_id", "classes", "time","result")


class UserAuditRecordSerialize_Retrieve(serializers.ModelSerializer):
    """
    操作日志---retrieve
    """

    class Meta:
        model = UserAuditRecordModel
        fields = "__all__"

# endregion

# region 用户权限信息 序列化器
class PermissionInforSerialize_List(serializers.ModelSerializer):
    """
    用户权限信息--list
    """
    class Meta:
        model = Permission
        fields =("id", "name", "codename")

# endregion

# region 用户组信息 序列化器
class GroupInforSerialize_Create(serializers.ModelSerializer):
    """
    用户组信息--create
    """
    class Meta:
        model = Group
        fields = "__all__"
   # 所有字段验证
    def validate(self, attrs):
        if not self.context['request'].user.has_perm('user.admin_userinformodel'):  # 如果当前用户有管理其他用户的权限
            raise serializers.ValidationError("当前用户不具备创建权限'")
        return attrs

class GroupInforSerialize_List(serializers.ModelSerializer):
    """
    用户组信息--list
    """
    permissions = PermissionInforSerialize_List(many=True)
    class Meta:
        model = Group
        fields =  "__all__"

# endregion
# region 用户信息 序列化器
class UserInforSerialize_Create(serializers.ModelSerializer):
    """
    用户信息--create
    """
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="密码", label="密码", write_only=True,)

    class Meta:
        model = User
        fields = ("id", "username", "password","auditor")


    def validate_auditor(self, value):
        try:
           auditor = User.objects.get(username=value)
        except Exception as e:
            raise serializers.ValidationError("指定的授权账号不存在")
        if not auditor.has_perm('user.admin_userinformodel'):
            raise serializers.ValidationError("指定的授权账号不具备授权权限")
        return value

    def create(self, validated_data):
        user = serializers.ModelSerializer.create(self,validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

class UserInforSerialize_List(serializers.ModelSerializer):
    """
    用户信息--list
    """
    class Meta:
        model = User
        fields = ("id", "username", "first_name","last_name","email",
                  "job_number","post","wechat","mobile","image","desc")

class UserInforSerialize_Retrieve(serializers.ModelSerializer):
    """
    用户信息--retrieve
    """

    groups=GroupInforSerialize_List(many=True)
    user_permissions=PermissionInforSerialize_List(many=True)
    all_permissions= serializers.SerializerMethodField()

    class Meta:
        model = User
        fields =( "id", "groups","user_permissions","last_login","is_superuser","username","first_name","last_name","email",
                    "is_staff","is_active", "date_joined","job_number","post","wechat","mobile","image",
                    "desc","auditor","create_time","update_time","all_permissions")

    #　获取添加的all_permissions字段信息
    def get_all_permissions(self, obj):
            permissions = self.instance.get_all_permissions()
            list_json = dict(zip(permissions, permissions))
            return list_json

class UserInforSerialize_Update(serializers.ModelSerializer):
    """
    用户信息--update
    """
    class Meta:
        model = User
        fields = ("id","groups","user_permissions", "first_name","last_name","email",
                  "job_number","post","wechat","mobile","image","desc")

    # 所有字段验证
    def validate(self, attrs):
        if self.instance.auditor == self.context['request'].user.username:  # 如果当前用户为指定的审核账号
            groups = attrs["groups"]
            user_permissions = attrs["user_permissions"]
            attrs = {"groups": groups,"user_permissions":user_permissions}
        elif self.instance.username == self.context['request'].user.username:  # 如果当前用户为创建者账号
            try:
                del attrs['groups']  # 删除groups字段
            except Exception:
                pass
            try:
                del attrs['user_permissions']  # 删除groups字段
            except Exception:
                pass
        else:
            raise serializers.ValidationError(self.instance.auditor+"的信息/权限不能被"+self.context['request'].user.username+"更改")
        return attrs

class UserInforSerialize_Partial(serializers.ModelSerializer):
    """
    用户信息--partial
    """

    class Meta:
        model = User
        fields = ("id", "password" )

    # 所有字段验证
    def validate(self, attrs):
        user = User.objects.get(username=self.instance.username)
        if self.context['request'].user.is_superuser:  # 如果用户为超级用户
            password = attrs["password"]
            if password is not "":
                user.set_password(password)
                attrs["password"]=user.password
        elif self.instance.username == self.context['request'].user.username:  # 如果当前用户为创建者账号
            password = attrs["password"]
            if password is not "":
                user.set_password(password)
                attrs["password"] = user.password
        else:
           raise serializers.ValidationError("登录用户非当前信息用户,不能对其更改密码")
        return attrs


# endregion


