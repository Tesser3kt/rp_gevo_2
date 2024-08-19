import logging
from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import viewsets
from .models import Profile
from .serializers import UserSerializer, ProfileSerializer, GroupSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
