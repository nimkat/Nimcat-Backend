import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from graphql_relay import from_global_id

from .graphene_permissions.mixins import AuthUserMutation
from .graphene_permissions.permissions import AllowAuthenticated
from .inputs import ProfileInputType
from .models import FollowingModel, ProfileModel
from .types import (ProfileType,
                    ProfileConnection)


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()  # For passwordless registration
    password_change = mutations.PasswordChange.Field()
    update_account = mutations.UpdateAccount.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = mutations.DeleteAccount.Field()
    # send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    # verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    # swap_emails = mutations.SwapEmails.Field()
    # remove_secondary_email = mutations.RemoveSecondaryEmail.Field()

    # django-graphql-jwt inheritances
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    profile = relay.Node.Field(ProfileType)
    all_profile = relay.ConnectionField(ProfileConnection)


class UpdateProfile(relay.ClientIDMutation):
    class Input:
        profile = graphene.Field(ProfileInputType)

    profile = graphene.Field(ProfileType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, profile):
        user = info.context.user
        profile, created = ProfileModel.objects.update_or_create(
            user=user, defaults={**profile})
        return UpdateProfile(profile=profile)

# in kheili zibast


class FollowOrUnfollow(AuthUserMutation, relay.ClientIDMutation):
    permission_classes = (AllowAuthenticated,)

    class Input:
        followed_id = graphene.ID(required=True)

    follow_status = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, followed_id):
        if cls.has_permission(root, info, input):
            user = info.context.user
            followed_id = from_global_id(followed_id)[1]
            status = FollowingModel.follow_or_unfollow(
                user=user, followed_id=followed_id)
            return FollowOrUnfollow(follow_status=status)
        return FollowOrUnfollow(follow_status=None)


class Mutation(AuthMutation, graphene.ObjectType):
    update_profile = UpdateProfile.Field()
    follow_or_unfollow = FollowOrUnfollow.Field()
    # social_auth = graphql_social_auth.relay.SocialAuth.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
