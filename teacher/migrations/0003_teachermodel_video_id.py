# Generated by Django 3.2.5 on 2021-07-05 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0002_alter_teachermodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='teachermodel',
            name='video_id',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
