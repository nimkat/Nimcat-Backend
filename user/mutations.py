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
from common.util.sms import send_verifiction_code


class RegisterSMS(graphene.Mutation):
    """Register user and send verification code"""

    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    class Input:
        mobile_number = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    def mutate(self, info, mobile_number, password1, password2, **kwargs):
        code = uuid.uuid1().int % 10000
        f = RegisterForm(mobile_number, password1, password2)
        if f.is_valid():
            user = f.save()
            UserStatus.objects.create(user=user)
            send_sms = send_verifiction_code(
                code=code, mobileNumber=mobile_number)
            SMSVerificationCodes.objects.create(user=user, code=code)

        else:
            return RegisterSMS(success=False, errors=f.errors.get_json_data())

        return RegisterSMS(success=True)


class VerifySMS(graphene.Mutation):
    """Verify user using verification code that send with sms"""

    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    class Input:
        mobile_number = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    def mutate(self, info, mobile_number, password1, password2, **kwargs):
        code = uuid.uuid1().int % 10000
        f = RegisterForm(mobile_number, password1, password2)
        if f.is_valid():
            user = f.save()
            UserStatus.objects.create(user=user)
            SMSVerificationCodes.objects.create(user=user, code=code)
        else:
            return RegisterSMS(success=False, errors=f.errors.get_json_data())

        return RegisterSMS(success=True)
