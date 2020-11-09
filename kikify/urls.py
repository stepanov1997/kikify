from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_user, name="login_user"),
    path('logout/', logout_user, name="logout_user"),
    path('register/', register_user, name="register_user"),
    path('song/<int:song_id>/', getSongById, name="getSongById"),
    path('artists/', artists, name="artists"),
    path('albums/', albums, name="albums"),
    path('songs/', songs, name="songs"),
    path('artist/<int:artist_id>/albums/', albumsOfArtist, name="albumsOfArtist"),
    path('artist/<int:artist_id>/album/<int:album_id>/songs/', songsOfAlbum, name="songsOfAlbum"),
]
