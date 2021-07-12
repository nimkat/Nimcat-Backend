import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id


from .types import TeacherType


class Query(graphene.AbstractType):
    teacher = relay.Node.Field(TeacherType)
    all_techears = DjangoFilterConnectionField(TeacherType)


class Mutation(graphene.ObjectType):
    pass
