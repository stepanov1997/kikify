import base64

from kikify.models import Artist, Album, File, Song
from django.core.files import File as Files


def upload_song(infos):
    # Creating artist
    exists = True

    artists = list(Artist.objects.filter(name=infos['artist']))
    artist = None
    if len(artists) == 0:
        exists = True
        artist = Artist.objects.create(name=infos['artist'])
    else:
        artist = artists[0]

    file_picture = base64.b64decode(infos['upload_art'])

    albums = list(Album.objects.filter(name=infos['album'],
                                       year_of_production=infos['year'],
                                       artist=artist))
    album = None
    if len(albums) == 0:
        album = Album(name=infos['album'],
                      year_of_production=infos['year'],
                      picture=file_picture)
        album.save()
        album.artist.add(artist)
    else:
        album = albums[0]

    # Creating song
    f = Files(file=open(infos["song"].temporary_file_path(), "rb"))

    files = list(File.objects.filter(file=f"{infos['title']} - {infos['album']} - {infos['artist']}.mp3"))
    file_song = None
    if len(files) == 0:
        file_song = File(name=f"{infos['title']} - {infos['album']} - {infos['artist']}.mp3",
                         type='song')
        file_song.file = f
        file_song.file.name = f"{infos['title']} - {infos['album']} - {infos['artist']}.mp3"
        print(infos['title'])
        file_song.save()
    else:
        file_song = files[0]

    songs = list(Song.objects.filter(name=infos['title'],
                                     year_of_production=infos['year'],
                                     album=album))
    song = None
    if len(songs) == 0:
        exists = False
        song = Song.objects.create(name=infos['title'],
                                   year_of_production=infos['year'],
                                   album=album,
                                   song_in_bytes=file_song)
        song.save()
    else:
        song = songs[0]

    print(f'Song {song.name} has been saved successfully.')

    return (song.id, exists)

