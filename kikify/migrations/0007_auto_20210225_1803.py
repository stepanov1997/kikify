# Generated by Django 3.1.5 on 2021-02-25 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kikify', '0006_auto_20210225_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userprofileinfo',
            name='user_type',
        ),
    ]