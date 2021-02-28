# Generated by Django 3.1.5 on 2021-02-26 20:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kikify', '0008_auto_20210226_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='recordlabel',
            name='picture',
            field=models.ImageField(default=django.utils.timezone.now, upload_to='kikify/media/profile_pictures/'),
            preserve_default=False,
        ),
    ]
