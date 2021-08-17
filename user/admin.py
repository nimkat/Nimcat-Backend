from user.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, ProfileModel, SMSVerificationCodes, BoughtCoursesModel

admin.site.register(User,UserAdmin)
admin.site.register(ProfileModel)
admin.site.register(SMSVerificationCodes)
admin.site.register(BoughtCoursesModel)
