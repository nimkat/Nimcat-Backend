from django.contrib import admin
from .models import CourseModel, CourseReviewModel, CourseCategoryModel

admin.site.register(CourseModel)
admin.site.register(CourseReviewModel)
admin.site.register(CourseCategoryModel)
