# Generated by Django 3.2.5 on 2021-07-21 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20210721_1413'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='courselessonmodel',
            options={'verbose_name': 'درس\u200c', 'verbose_name_plural': 'درس\u200cها'},
        ),
        migrations.AlterModelOptions(
            name='coursesectionmodel',
            options={'verbose_name': 'سرفصل\u200c', 'verbose_name_plural': 'سرفصل\u200cها'},
        ),
    ]
