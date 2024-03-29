from django.contrib import admin
from kikify.models import Song, Album, Artist, UserProfileInfo, RecordLabel, File


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("name", "year_of_production", "album", "song_in_bytes")


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ("name", "year_of_production")


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    pass


@admin.register(RecordLabel)
class RecordLabelAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfileInfo)
class UserProfileInfoAdmin(admin.ModelAdmin):
    pass


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass
