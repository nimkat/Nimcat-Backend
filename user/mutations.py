from course.models import CourseLessonModel, CourseModel
from graphql_auth.exceptions import GraphQLAuthError
from user.models import BoughtCoursesModel, SMSVerificationCodes
import graphene
from django.contrib.auth import get_user_model
from graphene import relay
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id
import uuid
from .forms import RegisterForm
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

    class Arguments:
        username = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            code = uuid.uuid1().int % 10000
            f = RegisterForm(kwargs)
            with transaction.atomic():
                if f.is_valid():
                    user = f.save()
                    send_sms = send_activation_sms(
                        code, kwargs.get(get_user_model().USERNAME_FIELD))
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

    class Arguments:
        code = graphene.String(required=True)
        username = graphene.String(required=True)

    @classmethod
    def mutate(self, info, root,  username, code, **kwargs):
        user = get_user_model().objects.get(username=username)
        if user == None:
            return VerifySMS(success=False, errors=_('User is invalid'))
        else:
            saved_code = SMSVerificationCodes.objects.get(code=code, user=user)
            if saved_code == None:
                return VerifySMS(success=False, errors=_('User not created, Register again'))
            else:
                saved_code.delete()
                setattr(user, 'verified', True)

        return VerifySMS(success=True)


class ResendSMS(graphene.Mutation):
    """Resend sms to user"""

    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    class Arguments:
        username = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):

        user = get_user_model().objects.get(
            username=kwargs.get(get_user_model().USERNAME_FIELD))
        if user == None:
            return ResendSMS(success=False, errors=_('User is invalid, register first'))
        else:
            code = uuid.uuid1().int % 10000
            SMSVerificationCodes.objects.filter(user=user).delete()
            send_sms = send_activation_sms(
                code, kwargs.get(get_user_model().USERNAME_FIELD))
            SMSVerificationCodes.objects.create(user=user, code=code)

        return ResendSMS(success=True)


class CompleteLesson(graphene.Mutation):
    """check course as completed"""

    success = graphene.Boolean()
    complete = graphene.Boolean()

    class Arguments:
        lesson_id = graphene.String(required=True)
        bought_course_id = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, lesson_id, bought_course_id):
        user = info.context.user
        lesson_pk = from_global_id(lesson_id)[1]
        bought_course_pk = from_global_id(bought_course_id)[1]

        lesson = CourseLessonModel.objects.get(pk=lesson_pk)
        bought_course = BoughtCoursesModel.objects.get(pk=bought_course_pk)

        if lesson in bought_course.complete_lessons.all():
            return CompleteLesson(success=True, complete=True)
        else:
            bought_course.complete_lessons.add(lesson)

        return CompleteLesson(success=True, complete=True)


class UndoCompleteLesson(graphene.Mutation):
    """uncheck course complete status"""

    success = graphene.Boolean()
    complete = graphene.Boolean()

    class Arguments:
        lesson_id = graphene.String(required=True)
        bought_course_id = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, lesson_id, bought_course_id):
        user = info.context.user
        lesson_pk = from_global_id(lesson_id)[1]
        bought_course_pk = from_global_id(bought_course_id)[1]
        lesson = CourseLessonModel.objects.get(pk=lesson_pk)
        bought_course = BoughtCoursesModel.objects.get(pk=bought_course_pk)

        if lesson in bought_course.complete_lessons.all():
            bought_course.complete_lessons.remove(lesson)
            return UndoCompleteLesson(success=True, complete=False)

        return UndoCompleteLesson(success=True, complete=False)
