# Generated by Django 3.1.5 on 2021-02-28 23:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kikify', '0012_auto_20210301_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(max_length=255, upload_to='songs/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='recordlabel',
            name='picture',
            field=models.ImageField(upload_to='profile_pictures/'),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='picture',
            field=models.ImageField(upload_to='profile_pictures/'),
        ),
    ]
