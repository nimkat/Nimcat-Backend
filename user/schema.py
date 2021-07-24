from graphene_django.filter.fields import DjangoFilterConnectionField
from user.mutations import RegisterSMS, ResendSMS, UndoCompleteLesson, VerifySMS, CompleteLesson
from course.models import CourseModel
import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphql_auth import mutations
from graphql_auth.schema import UserQuery, MeQuery
from graphql_relay import from_global_id

from django.utils.translation import gettext as _
from graphql import GraphQLError

from .graphene_permissions.mixins import AuthUserMutation
from .graphene_permissions.permissions import AllowAuthenticated
from .inputs import ProfileInputType
from .models import BoughtCoursesModel, ProfileModel
from .types import (BoughtCoursesType, ProfileType,
                    ProfileConnection, UserType)

from course.types import CourseType
# from .payment import send_payment_request


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


class MeUserQuery(MeQuery):
    me = graphene.Field(UserType)


class Query(UserQuery, MeUserQuery, graphene.ObjectType):
    profile = relay.Node.Field(ProfileType)
    all_profile = relay.ConnectionField(ProfileConnection)

    bought_course = relay.Node.Field(BoughtCoursesType)
    all_bought_courses = DjangoFilterConnectionField(BoughtCoursesType)

    secure_bougth_course = graphene.Field(
        BoughtCoursesType, id=graphene.String())
    my_bought_courses = DjangoFilterConnectionField(BoughtCoursesType)

    def resolve_secure_bougth_course(cls, info, id):
        user = info.context.user
        if user.is_authenticated:
            bought_courses_id = from_global_id(id)[1]
            bought_course = BoughtCoursesModel.objects.get(
                pk=bought_courses_id)
            if bought_course.user == user:
                if bought_course.payment_status == True:
                    return bought_course
                else:
                    return GraphQLError(_("َNot Payed"))
            else:
                return GraphQLError(_("Not Bought"))
        return GraphQLError(_("Not Authenticated"))

    def resolve_my_bought_courses(cls, info):
        user = info.context.user
        if user.is_authenticated:
            bought_courses = BoughtCoursesModel.objects.filter(
                user=user)
            return bought_courses
        return GraphQLError(_("Not Authenticated"))


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


# class GetPaymentLink(relay.ClientIDMutation):
#     class Input:
#         course_id = graphene.ID(required=True)

#     payment_url = graphene.String()

#     @classmethod
#     def mutate_and_get_payload(cls, root, info, course_id):
#         user = info.context.user
#         course = CourseModel.objects.get(pk=from_global_id(course_id)[1])
#         price = course.price
#         if course.discount_price is not None:
#             price = course.discount_price
#         payment_url = send_payment_request(amount=price)
#         return GetPaymentLink(payment_url=payment_url)


# class VerifyPayment(relay.ClientIDMutation):
#     class Input:
#         ref_id = graphene.String()
#         status = graphene.String()


#     @classmethod
#     def mutate_and_get_payload(cls, root, info):
#         pass


class Mutation(AuthMutation, graphene.ObjectType):
    update_profile = UpdateProfile.Field()
    buy_course = UpdateProfile.Field()
    # social_auth = graphql_social_auth.relay.SocialAuth.Field()
    register_sms = RegisterSMS.Field()
    verify_sms = VerifySMS.Field()
    resend_sms = ResendSMS.Field()
    complete_lesson = CompleteLesson.Field()
    undo_complete_lesson = UndoCompleteLesson.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
