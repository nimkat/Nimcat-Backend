from graphql_auth.exceptions import GraphQLAuthError
from user.models import SMSVerificationCodes
import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import uuid
from graphql_auth.models import UserStatus
from graphql_auth.forms import RegisterForm
from graphql_auth.types import ExpectedErrorType
from common.util.sms import send_activation_sms
from django.db import transaction
from django.utils.translation import gettext as _


class PhoneAlreadyInUse(GraphQLAuthError):
    default_message = _("This phone is already in use.")


class RegisterSMS(graphene.Mutation):
    """Register user and send verification code"""

    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    class Input:
        mobile_number = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    def mutate(self, info, mobile_number, password1, password2, **kwargs):
        try:
            code = uuid.uuid1().int % 10000
            f = RegisterForm(mobile_number, password1, password2)
            with transaction.atomic():
                if f.is_valid():
                    user = f.save()
                    UserStatus.objects.create(user=user)
                    send_sms = send_activation_sms(
                        code, mobile_number)
                    SMSVerificationCodes.objects.create(user=user, code=code)
                else:
                    return RegisterSMS(success=False, errors=f.errors.get_json_data())

                return RegisterSMS(success=True)

        except PhoneAlreadyInUse:
            return RegisterSMS(
                success=False,
                errors={get_user_model().USERNAME_FIELD: _(
                    'This phone is already in use.')},
            )


class VerifySMS(graphene.Mutation):
    """Verify user using verification code that send with sms"""

    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    class Input:
        code = graphene.String(required=True)
        mobile_number = graphene.String(required=True)

    def mutate(self, info, mobile_number, code, **kwargs):
        user = get_user_model().objects.get(mobile_number=mobile_number)
        if user == None:
            return RegisterSMS(success=False, errors=_('User is invalid'))
        else:
            saved_code = SMSVerificationCodes.objects.get(code=code, user=user)
            if saved_code == None:
                return RegisterSMS(success=False, errors=_('User not created, Register again'))
            else:
                saved_code.delete()
                status = UserStatus.objects.get(user=user)
                setattr(status, 'verified', True)

        return VerifySMS(success=True)
