from user.models import User
from django.contrib import admin
from .models import User, ProfileModel

admin.site.register(User)
admin.site.register(ProfileModel)
