import graphene
from graphene_file_upload.scalars import Upload


class ProfileInputType(graphene.InputObjectType):
    about = graphene.String()
    header = Upload()
    trip_status = graphene.Boolean()
    gender = graphene.String()  # must convert to enum implementation
