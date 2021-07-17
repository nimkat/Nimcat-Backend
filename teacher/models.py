from django.db import models
from django.contrib.auth import get_user_model


class TeacherModel(models.Model):
    class Meta:
        verbose_name = 'استاد'
        verbose_name_plural = 'اساتید'

    user = models.OneToOneField(
        to=get_user_model(), on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    en_name = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=200, blank=True)
    short_description = models.TextField(
        blank=True, null=True, max_length=1000)
    resume = models.JSONField(null=True, blank=True)
    video_id = models.CharField(max_length=100, blank=True)
    categories = models.ManyToManyField(
        to="course.CourseCategoryModel", blank=True, related_name="teacher_in_category")

    def __str__(self):
        return str(self.name)
