from graphene import relay
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from .models import (
    TeacherModel
)


class TeacherType(DjangoObjectType):
    class Meta:
        model = TeacherModel
        interfaces = (relay.Node,)
        filter_fields = ['categories']
        fields = "__all__"
