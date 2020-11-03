import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kikify_django.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django
import base64

django.setup()

from kikify.models import Artist, Album, Song, File
from django.utils import timezone
import stagger
from stagger.id3 import *  # contains ID3 frame types
from django.core.files import File as Files

def mp3gen(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                yield os.path.join(root, filename)


PATH = 'C:\\Users\\Kristijan\\Desktop\\Muzika'


def parseTag(tag):
    """
    Parse tag from mp3 file
    :param tag: mp3 tag
    :return: Dictionary of parsed elements (song, album, artist, year, picture)
    """
    artist_tag = None
    try:
        artist_tag = tag.artist
        if not artist_tag:
            artist_tag = 'Unknown artist'
    except:
        artist_tag = 'Unknown artist'

    album_tag = None
    try:
        album_tag = tag.album
        if not album_tag:
            album_tag = 'Unknown album'
    except:
        album_tag = 'Unknown album'

    song_tag = None
    try:
        song_tag = tag.title
        if not song_tag:
            song_tag = 'Unknown song'
    except:
        song_tag = 'Unknown song'

    year = None
    try:
        year = int(tag.date.split(sep='-')[0])
    except ValueError:
        year = 2020

    # picture = None
    # try:
    #     picture_file = tag.picture
    #     if not picture:
    #         picture_file = open('static/no-album-art.png', 'rb').read()
    #     encoded_picture = base64.b64encode(picture_file)
    # except:
    #     picture_file = open('static/no-album-art.png', 'rb').read()
    #     encoded_picture = base64.b64encode(picture_file)

    return {
        'song': song_tag,
        'album': album_tag,
        'artist': artist_tag,
        'year': year,
        # 'picture': encoded_picture
    }


for mp3file in mp3gen(PATH):

    tag = None
    try:
        tag = stagger.read_tag(mp3file)
    except:
        continue
    if not tag: continue

    parsedTag = parseTag(tag=tag)

    # Creating artist
    artists = list(Artist.objects.filter(name=parsedTag['artist']))
    artist = None
    if len(artists) == 0:
        artist = Artist.objects.create(name=parsedTag['artist'])
    else:
        artist = artists[0]

    # Creating album
    # files = list(File.objects.filter(bytes=parsedTag['picture']))
    # file_picture = None
    # if len(files) == 0:
    #     file_picture = File(bytes=parsedTag['picture'],
    #                         name=parsedTag['album'],
    #                         type='album_artwork')
    #     file_picture.save()
    # else:
    #     file_picture = files[0]

    albums = list(Album.objects.filter(name=parsedTag['album'],
                                       year_of_production=parsedTag['year'], artist=artist))
                                       # picture=file_picture))
    album = None
    if len(albums) == 0:
        album = Album(name=parsedTag['album'],
                      year_of_production=parsedTag['year'])
                      # picture=file_picture)
        album.save()
        album.artist.add(artist)
    else:
        album = albums[0]
        # picture = parsedTag['picture']

    # Creating song
    f = Files(open(mp3file, 'rb'))

    files = list(File.objects.filter(file=mp3file))
    file_song = None
    if len(files) == 0:
        file_song = File(name=parsedTag['song'],
                         type='song')
        file_song.file = f
        file_song.file.name=parsedTag['song']
        file_song.save()
    else:
        file_song = files[0]

    songs = list(Song.objects.filter(name=parsedTag['song'],
                                     year_of_production=parsedTag['year'],
                                     album=album))
    song = None
    if len(songs) == 0:
        song = Song.objects.create(name=parsedTag['song'],
                                   year_of_production=parsedTag['year'],
                                   album=album,
                                   song_in_bytes=file_song)
        song.save()
    else:
        song = songs[0]

    print(f'Song {song.name} has been saved successfully.')
