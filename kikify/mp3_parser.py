import base64
import random
import time
from django.core.files.storage import default_storage
from mutagen import File
from mutagen.mp3 import Open

from kikify_django import settings


def parse_tags(tags, file_name, file):
    """
    Parse tag from mp3 file
    :param file_name:
    :param tags: mp3 tag
    :return: Dictionary of parsed elements (song, album, artist, year, picture)
    """
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
        picture_file = extract_picture(file)
        if not picture_file:
            picture_file = open(str(settings.BASE_DIR) + '/kikify/static/no-album-art.png', 'rb').read()
        encoded_picture = base64.b64encode(picture_file)
    except Exception as e:
        picture_file = open(str(settings.BASE_DIR) + '/kikify/static/no-album-art.png', 'rb').read()
        encoded_picture = base64.b64encode(picture_file)

    return {
        'song': song_tag,
        'album': album_tag,
        'artist': artist_tag,
        'year': year,
        'picture': str(encoded_picture)[2:-1]
    }


def extract_picture(mp3):
    global tags

    help = round(time.time()*1000)

    with default_storage.open(f'{help}.mp3', 'wb+') as destination:
        for chunk in mp3.chunks():
            destination.write(chunk)

        file = File(default_storage.path(f'{help}.mp3'))
        artwork = file.tags['APIC:'].data

    default_storage.delete(f'{help}.mp3')

    if not artwork:
        return None
    return artwork
