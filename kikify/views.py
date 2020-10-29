from django.shortcuts import render
from django.http import HttpResponse
from .models import Song, Album, Artist
import base64

def index(request):
    print(Song.objects.all())
    dictionary = {
        'songs': Song.objects.all()
    }
    return render(request, 'kikify/home.html', dictionary)


def getSongById(request, id):
    song = Song.objects.filter(id=id).first().song_in_bytes
    decoded = base64.b64decode(song)
    return HttpResponse(content=decoded, content_type='audio/mp3')

