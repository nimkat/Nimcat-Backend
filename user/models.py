from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _

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

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(blank=True, upload_to='profiles/avatar')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


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
