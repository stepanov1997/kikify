from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login', login_user, name="login_user"),
    path('logout', logout_user, name="logout_user"),
    path('reset_password', reset_password, name="reset_password"),
    path('change_password', change_password, name="change_password"),
    path('register', register_menu, name="register_menu"),
    path('choose_type', choose_type, name="choose_type"),
    path('register/record_label', register_record_label, name="register_record_label"),
    path('register/user', register_user, name="register_user"),
    path('song/<int:song_id>', getSongById, name="getSongById"),
    path('album/<int:album_id>', getAlbumById, name="getAlbumById"),
    path('artist/<int:artist_id>', getArtistById, name="getArtistById"),
    path('deleteSong/<int:song_id>', deleteSong, name="deleteSong"),
    path('editSong', editSong, name="editSong"),
    path('deleteAlbum/<int:album_id>', deleteAlbum, name="deleteAlbum"),
    path('editAlbum', editAlbum, name="editAlbum"),
    path('deleteArtist/<int:artist_id>', deleteArtist, name="deleteArtist"),
    path('editArtist', editArtist, name="editArtist"),
    path('editProfile', editProfile, name="editProfile"),
    path('update_password', update_password, name="update_password"),
    path('artists', artists, name="artists"),
    path('albums', albums, name="albums"),
    path('songs', songs, name="songs"),
    path('get_music_info', get_music_info, name="get_music_info"),
    path('upload_song', upload_song, name="upload_song"),
    path('upload_album', upload_album, name="upload_album"),
    path('artist/<int:artist_id>/albums', albumsOfArtist, name="albumsOfArtist"),
    path('artist/<int:artist_id>/album/<int:album_id>/songs', songsOfAlbum, name="songsOfAlbum"),
]
