from .models import Organization
from .models import UserProfile

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class OrganizationModelSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"


class UserProfileModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ("password", )
        depth = 1
