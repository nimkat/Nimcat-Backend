# Generated by Django 3.2.5 on 2021-07-19 11:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courselikemodel',
            name='course',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_likes', to='course.coursemodel'),
        ),
        migrations.AlterField(
            model_name='courselikemodel',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='user_course_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
