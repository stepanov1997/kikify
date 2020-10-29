from django.db import models


class Song(models.Model):
    name = models.CharField(blank=False, max_length=255)
    year_of_production = models.IntegerField(blank=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    song_in_bytes = models.BinaryField(blank=False)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(blank=False, max_length=255)
    year_of_production = models.IntegerField(blank=True)
    picture = models.BinaryField()
    artist = models.ManyToManyField('Artist')

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(blank=False, max_length=255)

    def __str__(self):
        return self.name
