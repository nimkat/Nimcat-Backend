# Generated by Django 3.1.7 on 2021-07-18 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCategoryModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('short_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='course_category/')),
            ],
            options={
                'verbose_name': 'موضوع',
                'verbose_name_plural': 'موضوعات',
            },
        ),
        migrations.CreateModel(
            name='CourseLessonModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modify_at', models.DateTimeField(auto_now=True)),
                ('short_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('published', models.BooleanField(default=True)),
                ('video', models.CharField(blank=True, max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='CourseLikeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='CourseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('short_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='course/')),
                ('language', models.CharField(blank=True, choices=[('fa', 'فارسی'), ('en', 'English')], max_length=2, null=True)),
                ('price', models.BigIntegerField(blank=True, null=True)),
                ('discount_price', models.BigIntegerField(blank=True, null=True)),
                ('published', models.BooleanField(default=True)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('video', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'دوره',
                'verbose_name_plural': 'دوره\u200cها',
            },
        ),
        migrations.CreateModel(
            name='CourseReviewLikeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(choices=[(1, 'Up'), (-1, 'Down')])),
            ],
        ),
        migrations.CreateModel(
            name='CourseReviewModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('likes_count', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'نقد دوره\u200c',
                'verbose_name_plural': 'نقد\u200cهای دوره',
            },
        ),
        migrations.CreateModel(
            name='CourseSectionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('short_description', models.TextField(blank=True, max_length=1000, null=True)),
                ('published', models.BooleanField(default=True)),
                ('video', models.CharField(blank=True, max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100)),
                ('lessons', models.ManyToManyField(related_name='section_of_lesson', to='course.CourseLessonModel')),
            ],
        ),
    ]
