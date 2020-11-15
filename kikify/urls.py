from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    re_path('login', login_user, name="login_user"),
    path('logout', logout_user, name="logout_user"),
    path('reset_password', reset_password, name="reset_password"),
    path('change_password', change_password, name="change_password"),
    path('register', register_user, name="register_user"),
    path('song/<int:song_id>', getSongById, name="getSongById"),
    path('artists', artists, name="artists"),
    path('albums', albums, name="albums"),
    path('songs', songs, name="songs"),
    path('artist/<int:artist_id>/albums', albumsOfArtist, name="albumsOfArtist"),
    path('artist/<int:artist_id>/album/<int:album_id>/songs', songsOfAlbum, name="songsOfAlbum"),
]
