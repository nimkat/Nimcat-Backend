
import graphene
from graphene_django import DjangoObjectType

import graphql_jwt


import user.schema
import course.schema


class Query(
        user.schema.Query,
        course.schema.Query,
        graphene.ObjectType):
    pass


class Mutation(
    user.schema.Mutation,
    course.schema.Mutation,
    graphene.ObjectType,
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
