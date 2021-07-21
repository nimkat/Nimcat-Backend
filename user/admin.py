from user.models import User
from django.contrib import admin
from .models import User, ProfileModel, SMSVerificationCodes, BoughtCoursesModel

admin.site.register(User)
admin.site.register(ProfileModel)
admin.site.register(SMSVerificationCodes)
admin.site.register(BoughtCoursesModel)
