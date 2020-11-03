from django.shortcuts import render
from django.http import HttpResponse
from .models import Song, Album, Artist
from ranged_fileresponse import RangedFileResponse
import stagger
import base64


def index(request):
    print(Song.objects.all())
    dictionary = {
        'songs': Song.objects.all()
    }
    return render(request, 'kikify/htmls/home.html', dictionary)


def getSongById(request, id):
    song_path = Song.objects.filter(id=id).first().song_in_bytes.file
    response = RangedFileResponse(request, open(f"kikify/{song_path}", 'rb'), content_type='audio/*')
    response['Content-Disposition'] = f'attachment; filename="kikify/{song_path}"'
    return response


def getPictureBySongId(request, id):
    song_path = Song.objects.filter(id=id).first().song_in_bytes.file
    picture = None
    try:
        picture_file = stagger.read_tag(f"kikify/{song_path}").picture
        if not picture:
            picture_file = open('kikify/static/no-album-art.png', 'rb').read()
    except:
        picture_file = open('kikify/static/no-album-art.png', 'rb').read()
    return HttpResponse(content=picture_file, content_type='image/*')
