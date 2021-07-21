# Generated by Django 3.2.5 on 2021-07-19 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('teacher', '0001_initial'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursereviewmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course_review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursereviewmodel',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursemodel'),
        ),
        migrations.AddField(
            model_name='coursereviewlikemodel',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.coursereviewmodel'),
        ),
        migrations.AddField(
            model_name='coursereviewlikemodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='coursemodel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.coursecategorymodel'),
        ),
        migrations.AddField(
            model_name='coursemodel',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='course_of_section', to='course.CourseSectionModel'),
        ),
        migrations.AddField(
            model_name='coursemodel',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='teacher.teachermodel'),
        ),
        migrations.AddField(
            model_name='courselikemodel',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='course_likes', to='course.coursemodel'),
        ),
        migrations.AddField(
            model_name='courselikemodel',
            name='users',
            field=models.ManyToManyField(related_name='user_course_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
