import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kikify_django.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django
import base64
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import Open
django.setup()

from kikify.models import *
from django.core.files import File as Files

print(settings.MEDIA_ROOT)

files = list(File.objects.all())
for file in files:
    file.file.name = file.file.name[13:]
    file.save()


def mp3gen(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            if os.path.splitext(filename)[1] == ".mp3":
                yield os.path.join(root, filename)


PATH = 'C:\\Users\\stepa\\Desktop\\Desktop (HP)\\Muzika'


def parseTag2(tags, path):
    """
    Parse tag from mp3 file
    :param tags: mp3 tag
    :return: Dictionary of parsed elements (song, album, artist, year, picture)
    """
    file_name = path.split("\\")[-1]
    artist_tag = None
    try:
        artist_tag = tags["artist"][0]
        if not artist_tag:
            artist_tag = file_name.split("-")[0]
    except:
        artist_tag = 'Unknown artist'

    album_tag = None
    try:
        album_tag = tags["album"][0]
        if not album_tag:
            album_tag = 'Unknown album'
    except:
        album_tag = 'Unknown album'

    song_tag = None
    try:
        song_tag = tags["title"][0]
        if not song_tag:
            song_tag = file_name.split("-")[-1]
    except:
        song_tag = file_name

    year = None
    try:
        year = int(tags["date"][0].split(sep='-')[0])
    except:
        year = 2020

    picture_file = None
    try:
        picture_file = extract_picture(path)
        if not picture_file:
            picture_file = open('static/no-album-art.png', 'rb').read()
        encoded_picture = base64.b64encode(picture_file)
    except:
        picture_file = open('static/no-album-art.png', 'rb').read()
        encoded_picture = base64.b64encode(picture_file)

    return {
        'song': song_tag,
        'album': album_tag,
        'artist': artist_tag,
        'year': year,
        'picture': encoded_picture
    }


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

    picture = None
    try:
        picture_file = tag.picture
        if not picture:
            picture_file = open('static/no-album-art.png', 'rb').read()
        encoded_picture = base64.b64encode(picture_file)
    except:
        picture_file = open('static/no-album-art.png', 'rb').read()
        encoded_picture = base64.b64encode(picture_file)

    return {
        'song': song_tag,
        'album': album_tag,
        'artist': artist_tag,
        'year': year,
        'picture': encoded_picture
    }


def extract_picture(mp3):
    try:
        tags = Open(mp3)
    except Exception as e:
        print(e)
    data = ""
    for i in tags:
        if i.startswith("APIC"):
            data = tags[i].data
            break
    if not data:
        return None
    return data


for mp3file in mp3gen(PATH):

    tag = None
    try:
        # tag = stagger.read_tag(mp3file)
        tag = EasyID3(mp3file)
    except:
        continue
    if not tag: continue

    # parsedTag = parseTag(tag=tag)

    parsedTag = parseTag2(tags=tag, path=mp3file)

    # Creating artist
    artists = list(Artist.objects.filter(name=parsedTag['artist']))
    artist = None
    if len(artists) == 0:
        artist = Artist.objects.create(name=parsedTag['artist'])
    else:
        artist = artists[0]

    file_picture = parsedTag['picture']

    albums = list(Album.objects.filter(name=parsedTag['album'],
                                       year_of_production=parsedTag['year'],
                                       artist=artist,
                                       picture=file_picture))
    album = None
    if len(albums) == 0:
        album = Album(name=parsedTag['album'],
                      year_of_production=parsedTag['year'],
                      picture=file_picture)
        album.save()
        album.artist.add(artist)
    else:
        album = albums[0]

    # Creating song
    f = Files(open(mp3file, 'rb'))

    files = list(File.objects.filter(file=mp3file))
    file_song = None
    if len(files) == 0:
        file_song = File(name=parsedTag['song'],
                         type='song')
        file_song.file = f
        file_song.file.name = mp3file.split("\\")[-1]
        print(parsedTag['song'])
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
