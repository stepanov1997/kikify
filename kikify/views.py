from django.shortcuts import render
from django.http import HttpResponse
from .models import Song, Album, Artist
from ranged_fileresponse import RangedFileResponse
import stagger
import base64


def index(request):
    # def mapSongs(song):
    #     song.album.picture = str(song.album.picture)
    #     print(song.album.picture)
    #     return song
    # print(list(map(mapSongs, Song.objects.all())))
    dictionary = {
        'songs': Song.objects.all()
    }
    return render(request, 'kikify/htmls/home.html', dictionary)


def artists(request):
    dictionary = {
        'artists': Artist.objects.all()
    }
    return render(request, 'kikify/htmls/artists.html', dictionary)


def albumsOfArtist(request, id):
    dictionary = {
        'albums': Album.objects.filter(artist__id=id),
        'artist': Artist.objects.filter(id=id).first()
    }
    return render(request, 'kikify/htmls/albumsOfArtist.html', dictionary)


def songsOfAlbums(request, artistId, albumId):
    dictionary = {
        'songs': Song.objects.filter(album__id=albumId),
        'artist': Artist.objects.filter(id=artistId),
        'album': Album.objects.filter(id=albumId)
    }
    print(dictionary)
    return render(request, 'kikify/htmls/songsOfAlbum.html', dictionary)


def getSongById(request, id):
    song_path = Song.objects.filter(id=id).first().song_in_bytes.file
    response = RangedFileResponse(request, open(f"kikify/{song_path}", 'rb'), content_type='audio/*')
    response['Content-Disposition'] = f'attachment; filename="kikify/{song_path}"'
    return response
