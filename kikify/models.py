from django.db import models
import time


class File(models.Model):
    name = models.CharField(blank=False, max_length=255)
    type = models.CharField(blank=False, max_length=100)
    file = models.FileField(upload_to='media/songs/%Y/%m/%d/', max_length=255)


class Song(models.Model):
    name = models.CharField(blank=False, max_length=255)
    year_of_production = models.IntegerField(blank=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    song_in_bytes = models.OneToOneField('File', blank=False, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(blank=False, max_length=255)
    year_of_production = models.IntegerField(blank=True)
    # picture = models.ForeignKey('File', blank=False, on_delete=models.CASCADE)
    artist = models.ManyToManyField('Artist')

    def __unicode__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __unicode__(self):
        return self.name
