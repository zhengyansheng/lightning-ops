from .models import Role
from .models import PermRule
from .models import RoleBind
from .models import Router
from apps.user.models import UserProfile

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, exceptions


class RoleModelSerializer(ModelSerializer):

    def validate(self, attrs):
        role_name = attrs['name']
        if not role_name.endswith(":role"):
            attrs['name'] = role_name + ':role'
        return attrs

    class Meta:
        model = Role
        fields = "__all__"
        extra_kwargs = {
            "name": {
                "required": True
            }
        }


class PermRuleModelSerializer(ModelSerializer):
    # role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)

    class Meta:
        model = PermRule
        exclude = ("ptype",)
        depth = 1
        extra_kwargs = {
            "ptype": {
                "read_only": True
            },
            "name": {
                "required": True
            },
            "user": {
                "required": True
            },
            "role": {
                "required": True
            },
        }


class RolePermSerializer(serializers.Serializer):
    perm = serializers.PrimaryKeyRelatedField(queryset=PermRule.objects.all(), many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RoleRouteSerializer(serializers.Serializer):
    route = serializers.PrimaryKeyRelatedField(queryset=Router.objects.all(), many=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserRoleBindSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all())
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)

    def create(self, validated_data):
        bulk_role_bind = [RoleBind(user=validated_data['user'], role=role) for role in validated_data['role']]
        return RoleBind.objects.bulk_create(bulk_role_bind)

    def save(self, **kwargs):
        pass

    def update(self, instance, validated_data):
        pass


class RoleBindModelSerializer(ModelSerializer):
    class Meta:
        model = RoleBind
        extra_kwargs = {
            "ptype": {
                "read_only": True
            },
            "user": {
                "required": True
            },
            "role": {
                "required": True
            },
        }
        exclude = ("ptype",)


class HasPermSerializer(serializers.Serializer):
    path = serializers.CharField(required=True)
    method = serializers.CharField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class RouterSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        parent = attrs.get('parent')
        is_parent = attrs.get('isParent', True)
        if parent is None:
            if is_parent is not True:
                raise exceptions.ValidationError({"isParent": ["parent为None, isParent期待True"]})
        if parent is not None:
            if is_parent is True:
                raise exceptions.ValidationError({"isParent": ["isParent期待False"]})
        return attrs

    def to_representation(self, instance):
        ret = super(RouterSerializer, self).to_representation(instance)
        try:
            ret.pop('parent')
        except KeyError:
            pass

        try:
            ret.pop('isParent')
        except KeyError:
            pass

        return ret

    class Meta:
        model = Router
        exclude = ("create_time", "update_time", "remark", "role")
