# Generated by Django 3.1.2 on 2020-12-03 13:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kikify', '0002_auto_20201203_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='name',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]