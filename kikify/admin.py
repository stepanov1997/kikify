from django.contrib import admin
from kikify.models import Song, Album, Artist

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("name", "year_of_production", "album", "song_in_bytes")

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass

