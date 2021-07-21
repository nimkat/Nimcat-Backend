from django.contrib import admin
from .models import CourseModel, CourseReviewModel, CourseCategoryModel, CourseSectionModel, CourseLessonModel

admin.site.register(CourseModel)
admin.site.register(CourseSectionModel)
admin.site.register(CourseLessonModel)
admin.site.register(CourseReviewModel)
admin.site.register(CourseCategoryModel)
