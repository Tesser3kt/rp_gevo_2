from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Profile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.HyperlinkedRelatedField(
        view_name="profile-detail", read_only=True
    )

    class Meta:
        model = User
        fields = ["url", "id", "username", "profile"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    group = serializers.HyperlinkedRelatedField(
        view_name="group-detail", read_only=True
    )

    class Meta:
        model = Group
        fields = ["url", "id", "name", "group"]


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(view_name="user-detail", read_only=True)

    class Meta:
        model = Profile
        fields = ["url", "user", "cls"]
