# Generated by Django 3.2.5 on 2021-07-12 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_auto_20210705_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='course_of_section', to='course.CourseSectionModel'),
        ),
    ]
