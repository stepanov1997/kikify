# Generated by Django 3.1.5 on 2021-03-12 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kikify', '0013_auto_20210301_0006'),
    ]

    operations = [
        migrations.RenameField(
            model_name='album',
            old_name='artist',
            new_name='artists',
        ),
        migrations.AddField(
            model_name='artist',
            name='albums',
            field=models.ManyToManyField(to='kikify.Album'),
        ),
    ]
