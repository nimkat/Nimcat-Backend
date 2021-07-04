from django.contrib import admin
from .models import CourseModel, CourseReviewModel, CategoryModel

admin.site.register(CourseModel)
admin.site.register(CourseReviewModel)
admin.site.register(CategoryModel)
