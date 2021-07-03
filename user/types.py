import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import get_user_model
from graphene import relay

from .models import AchievementModel, FollowingModel, ProfileModel


class FollowingType(DjangoObjectType):
    class Meta:
        model = FollowingModel
        filter_fields = "__all__"
        interfaces = (relay.Node, )
        fields = "__all__"


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        filter_exclude = ["avatar"]
        interfaces = (relay.Node, )
        fields = "__all__"


class ProfileType(DjangoObjectType):

    def resolve_avatar(self, info):
        """Resolve avatar image absolute path"""
        if self.avatar:
            self.avatar = info.context.build_absolute_uri(self.avatar.url)
        return self.avatar

    def resolve_header(self, info):
        """Resolve header image absolute path"""
        if self.header:
            self.header = info.context.build_absolute_uri(self.header.url)
        return self.header

    class Meta:
        model = ProfileModel
        interfaces = (relay.Node, )
        fields = "__all__"


class ProfileConnection(relay.Connection):

    class Meta:
        node = ProfileType


class AchivmentType(DjangoObjectType):
    class Meta:
        model = AchievementModel
        interfaces = (relay.Node, )
        fields = "__all__"