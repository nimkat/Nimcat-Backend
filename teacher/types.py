from graphene import relay
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from .models import (
    TeacherModel
)


class TeacherType(DjangoObjectType):
    class Meta:
        model = TeacherModel
        # filter_fields = "__all__"
        interfaces = (relay.Node,)
        fields = "__all__"
