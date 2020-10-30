from django.shortcuts import render
from django.http import HttpResponse
from .models import Song, Album, Artist
import base64


def index(request):
    print(Song.objects.all())
    dictionary = {
        'songs': Song.objects.all()
    }
    return render(request, 'kikify/htmls/home.html', dictionary)


def getSongById(request, id):
    song = Song.objects.filter(id=id).first().song_in_bytes.bytes
    return HttpResponse(content=song, content_type='audio/mp3')


def getPictureByAlbumId(request, id):
    picture = Album.objects.filter(id=id).first().picture.bytes
    decoded_picture = base64.b64decode(picture)
    return HttpResponse(content=decoded_picture, content_type='image/png')
