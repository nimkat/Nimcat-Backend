from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _
from common.util.mobileValidator import UnicodeMobileNumberValidator

GENDER = [
    ('m', 'male'),
    ('f', 'female'),
    ('o', 'non binary'),
]


class AchievementModel(models.Model):
    title = models.TextField(blank=True, max_length=200)
    image = models.ImageField(blank=True, upload_to='profiles/achivment')


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    # def _create_user(self, email, password, **extra_fields):
    #     """Create and save a User with the given email and password."""
    #     if not email:
    #         raise ValueError('The given email must be set')
    #     email = self.normalize_email(email)
    #     user = self.model(email=email, **extra_fields)
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user

    # def create_user(self, email, password=None, **extra_fields):
    #     """Create and save a regular User with the given email and password."""
    #     extra_fields.setdefault('is_staff', False)
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)

    # def create_superuser(self, email, password, **extra_fields):
    #     """Create and save a SuperUser with the given email and password."""
    #     extra_fields.setdefault('is_staff', True)
    #     extra_fields.setdefault('is_superuser', True)

    #     if extra_fields.get('is_staff') is not True:
    #         raise ValueError('Superuser must have is_staff=True.')
    #     if extra_fields.get('is_superuser') is not True:
    #         raise ValueError('Superuser must have is_superuser=True.')

    #     return self._create_user(email, password, **extra_fields)

    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The given username must be set')
        # email = self.normalize_email(email)
        username = self.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)

    def normalize_username(self, username):
        return username


class User(AbstractUser):

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    verified = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    email = models.EmailField(_('email address'), null=True, blank=True)
    avatar = models.ImageField(blank=True, upload_to='profiles/avatar')

    mobile_number_validator = UnicodeMobileNumberValidator()
    username = models.CharField(max_length=50,
                                unique=True,
                                verbose_name=_('Mobile Number'),
                                validators=[mobile_number_validator],
                                error_messages={
                                    'unique': _("A user with that mobile number already exists."),
                                },
                                null=True
                                )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.username == None:
            return "MOBILE NUMBER NULL"
        return self.username


class ProfileModel(models.Model):

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل‌ها'

    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, primary_key=True)
    about = models.TextField(blank=True, null=True, max_length=400)
    gender = models.CharField(
        choices=GENDER, max_length=2, blank=True, null=True)
    achievements = models.ManyToManyField(AchievementModel, blank=True)

    def __str__(self):
        return str(self.user)


def create_profile_for_user(sender, instance, **kwargs):
    if kwargs['created']:
        profile = ProfileModel.objects.create(user=instance)


post_save.connect(receiver=create_profile_for_user, sender=User)


class FavouriteCourseModel(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        "course.CourseModel", on_delete=models.CASCADE)


class BoughtCoursesModel(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE)
    course = models.ForeignKey(
        "course.CourseModel", on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    ref_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    complete_lessons = models.ManyToManyField(
        to="course.CourseLessonModel", related_name="users_completed", blank=True)


class SMSVerificationCodes(models.Model):
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE)
    code = models.CharField(max_length=4, null=True)

    def __str__(self):
        return self.user.username
