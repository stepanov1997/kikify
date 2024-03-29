import os

from django.db import models
from django.contrib.auth.models import User
import time

from kikify_django import settings


class ResetingPasswordQueue(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_pictures/')

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.user.username


class File(models.Model):
    name = models.CharField(blank=False, max_length=255)
    type = models.CharField(blank=False, max_length=100)
    file = models.FileField(upload_to='songs/%Y/%m/%d/', max_length=255)

    def __unicode__(self):
        return self.file.path

    def __str__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(blank=False, max_length=255)
    year_of_production = models.IntegerField(blank=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    song_in_bytes = models.OneToOneField('File', blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(blank=False, max_length=255)
    year_of_production = models.IntegerField(blank=True)
    picture = models.BinaryField()
    artist = models.ManyToManyField('Artist')
    record_label = models.ManyToManyField('RecordLabel')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class RecordLabel(models.Model):
    name = models.CharField(blank=False, max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    picture = models.ImageField(upload_to='profile_pictures/')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
