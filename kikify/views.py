import base64
import io
import json
import os
import secrets
import smtplib
import traceback
import zipfile
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponseRedirect, FileResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from mutagen.easyid3 import EasyID3
from ranged_fileresponse import RangedFileResponse
from requests import Response
import copy
from distutils.util import strtobool

from kikify.forms import UserForm, UserProfileInfoForm, RecordLabelForm
from kikify_django import settings
from . import song_service
from .models import Song, Album, RecordLabel, UserProfileInfo, ResetingPasswordQueue, Artist
from .mp3_parser import parse_tags
from zipfile import ZipFile

MY_ADDRESS = 'kristijan.stepanov@student.etf.unibl.org'
PASSWORD = 'cikakiki1997'
SITE_ROOT = 'http://localhost:8000/kikify/'


def register_menu(request):
    return render(request, 'kikify/htmls/register_menu.html', {})


def register_user(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.picture = request.FILES['profile_picture']

            profile.save()

            registered = True

            return render(request, 'kikify/htmls/login.html', {
                'successful': True,
                'message': "You successfully registered, please login."
            })
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context = {'user_form': user_form,
               'profile_form': profile_form,
               'registered': registered,
               'isUser': True
               }

    return render(request, 'kikify/htmls/register.html', context)


@transaction.atomic
def register_record_label(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        record_label_form = RecordLabelForm(data=request.POST)

        user = user_form.save()
        user.set_password(user.password)
        user.save()

        record_label = record_label_form.save(commit=False)
        record_label.user = user

        if 'profile_image' in request.FILES:
            record_label.picture = request.FILES['profile_image']

        record_label.save()

        registered = True

        return render(request, 'kikify/htmls/login.html', {
            'successful': True,
            'message': "You successfully registered, please login.",
            'post_request': request.method == 'POST'
        })

    else:
        user_form = UserForm(data=request.GET)
        record_label_form = RecordLabelForm(data=request.GET)

        context = {'user_form': user_form,
                   'successful': False,
                   'profile_form': record_label_form,
                   'registered': registered,
                   'isUser': False,
                   'post_request': request.method == 'POST'
                   }

        return render(request, 'kikify/htmls/register.html', context)


def record_label(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_picture' in request.FILES:
                profile.picture = request.FILES['profile_picture']

            profile.save()

            registered = True

            return render(request, 'kikify/htmls/login.html', {
                'successful': True,
                'message': "You successfully registered, please login.",
                'post_request': request.method == 'POST'
            })
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered,
        'isArtist': True,
        'post_request': request.method == 'POST'
    }

    return render(request, 'kikify/htmls/register.html', context)


def login_user(request):
    print(request)
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,
                            password=password)

        if user:
            types = []
            if UserProfileInfo.objects.filter(user__id=user.id).exists():
                types.append("USER")
            elif user.is_superuser:
                types.append("ADMIN")
            if RecordLabel.objects.filter(user__id=user.id).exists():
                types.append("RECORD_LABEL")

            if "ADMIN" in types:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            elif user.is_active and len(types) == 2:
                login(request, user)
                return HttpResponseRedirect(reverse('choose_type'))
            elif user.is_active and len(types) == 1 and types[0] == "USER":
                login(request, user)
                request.session['type'] = types[0]
                return HttpResponseRedirect(reverse('home'))
            elif user.is_active and len(types) == 1 and types[0] == "RECORD_LABEL":
                login(request, user)
                request.session['type'] = types[0]
                return HttpResponseRedirect(reverse('home'))
            else:
                return render(request, 'kikify/htmls/login.html', {
                    'username': username,
                    'successful': False,
                    'message': 'Account is not active.',
                    'post_request': request.method == 'POST'
                })
        else:
            userFiltered = User.objects.filter(username=username)
            if len(userFiltered) > 0:
                user = userFiltered.first()
                if user.is_active:
                    return render(request, 'kikify/htmls/login.html', {
                        'username': username,
                        'successful': False,
                        'message': 'Wrong username or password.',
                        'post_request': request.method == 'POST'
                    })
                else:
                    return render(request, 'kikify/htmls/login.html', {
                        'username': username,
                        'successful': False,
                        'message': 'Account is not active.',
                        'post_request': request.method == 'POST'
                    })
            else:
                print("Someone tried to login and failed!")
                return render(request, 'kikify/htmls/login.html', {
                    'username': username,
                    'successful': False,
                    'message': 'Wrong username or password.',
                    'post_request': request.method == 'POST'
                })
    else:
        return render(request, 'kikify/htmls/login.html', {
            'message': '-',
            'successful': True,
        })


@login_required
def choose_type(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        if type == "USER":
            request.session['type'] = type
            return redirect(to=home)
        elif type == "RECORD_LABEL":
            request.session['type'] = type
            return redirect(to=home)
        else:
            return render(request=request, template_name='kikify/htmls/choose_type.html')
    else:
        return render(request=request, template_name='kikify/htmls/choose_type.html')


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get("email")

        userProfileInfos = UserProfileInfo.objects.filter(user__email=email)
        if len(userProfileInfos) > 0:
            try:
                # set up the SMTP server
                s = smtplib.SMTP(host='smtp.gmail.com', port=587)
                s.starttls()
                s.login(MY_ADDRESS, PASSWORD)

                msg = MIMEMultipart()

                token = secrets.token_urlsafe(16)

                user = User.objects.filter(email=email).first()
                rpq = ResetingPasswordQueue(email=email, user=user, token=token)
                rpq.save()

                # setup the parameters of the message
                msg['From'] = MY_ADDRESS
                msg['To'] = email
                msg['Subject'] = "Kikify - reset password"
                html = f"""\
                <html>
                  <body>
                    <p>Hi, {user.username}<br>
                       Someone requested reseting password for this mail.<br><br>
                       If you did it, press link below: 
                       <a href="{SITE_ROOT}change_password?token={token}">Link for reseting password</a><br>
                       Otherwise ignore this email.
                    </p>
                    <p>
                       Kikify admin.
                    </p>
                  </body>
                </html>
                """
                mime = MIMEText(html, "html")
                # add in the message body
                msg.attach(mime)

                # send the message via the server set up earlier.
                s.sendmail(
                    MY_ADDRESS, email, msg.as_string()
                )
                del msg

                # Terminate the SMTP session and close the connection
                s.quit()
            except Exception:
                print(traceback.format_exc())
                return render(request, 'kikify/htmls/reset_password.html', {
                    'GET': False,
                    'email_exists': False,
                    'successful': False,
                    'message': "Email is unsuccessfully sent."
                })
            return render(request, 'kikify/htmls/reset_password.html', {
                'GET': False,
                'email_exists': True,
                'successful': True,
                'message': "Email is successfully sent."
            })
        else:
            return render(request, 'kikify/htmls/reset_password.html', {
                'GET': False,
                'email_exists': False,
                'successful': False,
                'message': "Email is unsuccessfully sent."
            })
    else:
        return render(request, 'kikify/htmls/reset_password.html', {'GET': True})


def change_password(request):
    # Otvaranje linka iz mejla
    if request.method == 'GET':
        token = request.GET.get("token")
        if token and len(token) > 0:
            obs = ResetingPasswordQueue.objects.filter(token=token)
            if len(obs) > 0:
                return render(request, 'kikify/htmls/change_password.html', {'token': token})
            else:
                return HttpResponseRedirect(reverse('reset_password'))
        else:
            return HttpResponseRedirect(reverse('reset_password'))
    else:
        token = request.POST.get("token")
        password = request.POST.get("password")
        password_again = request.POST.get("password_again")

        if token and len(token) > 0:
            obs = ResetingPasswordQueue.objects.filter(token=token)
            if len(obs) > 0:
                if password != password_again:
                    return render(request, 'kikify/htmls/change_password.html', {
                        'successful': False,
                        'message': "Passwords don't match each other."
                    })
                user = obs.first().user
                user.set_password(password)
                user.save()
                obs.delete()
                return render(request, 'kikify/htmls/login.html', {
                    'successful': True,
                    'message': 'You successfully changed password. <br>You can log in with new password.'
                })
        else:
            return HttpResponseRedirect(reverse('reset_password'))


@login_required
def home(request):
    global type
    if request.session.has_key('type'):
        type = request.session['type']

    isUser = type == 'USER'
    if request.user.username:
        user_profiles_info = UserProfileInfo.objects.filter(user__username=request.user.username)
        record_label_user = RecordLabel.objects.filter(user__username=request.user.username)
        if isUser and user_profiles_info and len(user_profiles_info) > 0 and user_profiles_info.first():
            user_profile_info = user_profiles_info.first()
            picture_path = None if not user_profile_info.picture else user_profile_info.picture.path
            picture = None
            try:
                with open(picture_path, 'rb') as f:
                    picture = f.read()
            except:
                pass
            context = {
                'user_image': None if not picture else str(base64.b64encode(picture), 'utf-8'),
                'username': user_profile_info.user.username,
                'about': "About",
                'isUser': isUser,
                'email': request.user.email,
                'firstname': request.user.first_name,
                'secondname': request.user.last_name,
                'isSuperuser': request.user.is_superuser
            }
            return render(request, 'kikify/htmls/home.html', context)
        elif not isUser and record_label_user and len(record_label_user) > 0 and record_label_user.first():
            record_label_user = record_label_user.first()
            picture_path = None if not record_label_user.picture else record_label_user.picture.path
            picture = None
            try:
                with open(picture_path, 'rb') as f:
                    picture = f.read()
            except:
                pass
            context = {
                'user_image': None if not picture else str(base64.b64encode(picture), 'utf-8'),
                'username': record_label_user.user.username,
                'name': record_label_user.name,
                'about': "About",
                'isUser': isUser,
                'firstname': request.user.first_name,
                'secondname': request.user.last_name,
                'email': request.user.email,
                'isSuperuser': request.user.is_superuser
            }
            return render(request, 'kikify/htmls/home.html', context)
        else:
            users = User.objects.filter(username=request.user.username)
            if users and len(users) > 0 and users.first() and users.first().is_superuser:
                context = {
                    'username': users.first().username,
                    'about': "About",
                    'isUser': isUser,
                    'email': request.user.email,
                    'firstname': request.user.first_name,
                    'secondname': request.user.last_name,
                    'isSuperuser': request.user.is_superuser
                }
                return render(request, 'kikify/htmls/home.html', context)
            else:
                return render(request, 'kikify/htmls/login.html', {
                    'successful': False,
                    'message': 'Please log in as user.',
                    'isUser': isUser,
                    'firstname': request.user.first_name,
                    'secondname': request.user.last_name,
                    'email': request.user.email,
                    'isSuperuser': request.user.is_superuser
                })
    else:
        return render(request, 'kikify/htmls/login.html', {
            'isUser': isUser,
            'isSuperuser': request.user.is_superuser,
            'email': request.user.email,
            'firstname': request.user.first_name,
            'secondname': request.user.last_name,
        })


@login_required
def artists(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    isRecordLabel = bool(body['isRecordLabel'])

    artists_list = Artist.objects.all()
    if not request.user.is_superuser and isRecordLabel:
        artists_list = Artist.objects.filter(album__record_label__user__id=request.user.id)
    else:
        artists_list = Artist.objects.all()

    dictionary = {
        'artists': artists_list,
        'isUser': not isRecordLabel,
        'isSuperuser': request.user.is_superuser
    }
    return render(request, 'kikify/components/artists.html', dictionary)


@login_required
def albums(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    isRecordLabel = bool(body['isRecordLabel'])

    if not request.user.is_superuser and isRecordLabel:
        albums_list = Album.objects.filter(record_label__user__id=request.user.id)
    else:
        albums_list = Album.objects.all()

    dictionary = {
        'albums': albums_list,
        'isUser': not isRecordLabel
    }
    return render(request, 'kikify/components/albums.html', dictionary)


@login_required
def songs(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    isRecordLabel = bool(body['isRecordLabel'])

    if not request.user.is_superuser and isRecordLabel:
        song_list = Song.objects.filter(album__record_label__user__id=request.user.id).all()
    else:
        song_list = Song.objects.all()

    dictionary = {
        'songs': song_list,
        'isUser': not isRecordLabel
    }

    return render(request, 'kikify/components/songs.html', dictionary)


@login_required
def albumsOfArtist(request, artist_id):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    isRecordLabel = bool(body['isRecordLabel'])

    if not request.user.is_superuser and isRecordLabel:
        dictionary = {
            'albums': Album.objects.filter(artist__id=artist_id, record_label__user__id=request.user.id),
            'RecordLabel': RecordLabel.objects.filter(id=artist_id).first(),
            'isUser': not isRecordLabel
        }
    else:
        dictionary = {
            'albums': Album.objects.filter(artist__id=artist_id),
            'RecordLabel': RecordLabel.objects.filter(id=artist_id).first(),
            'isUser': not isRecordLabel
        }

    return render(request, 'kikify/components/albums.html', dictionary)


@login_required
def songsOfAlbum(request, artist_id, album_id):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    isRecordLabel = bool(body['isRecordLabel'])

    if (not request.user.is_superuser) and isRecordLabel:
        dictionary = {
            'songs': Song.objects.filter(album__id=album_id, album__record_label__user=request.user),
            'RecordLabel': RecordLabel.objects.filter(id=artist_id),
            'album': Album.objects.filter(id=album_id, record_label__user=request.user),
            'isUser': not isRecordLabel
        }
    else:
        dictionary = {
            'songs': Song.objects.filter(album__id=album_id),
            'RecordLabel': RecordLabel.objects.filter(id=artist_id),
            'album': Album.objects.filter(id=album_id),
            'isUser': not isRecordLabel
        }

    return render(request, 'kikify/components/songs.html', dictionary)


@login_required
def get_music_info(request):
    mp3file = request.FILES['file']
    tag = None
    try:
        tag = EasyID3(mp3file)
    except:
        return HttpResponse(content={}, status=204)
    if not tag: return HttpResponse(content={}, status=204)

    # parsedTag = parseTag(tag=tag)

    url = request.build_absolute_uri('/')

    parsed_tags = parse_tags(tags=tag, file_name=mp3file.name, url=url, file=mp3file)
    json_response = json.dumps(parsed_tags)
    return HttpResponse(content=json_response, content_type='application/json')


@login_required
def upload_song(request):
    song = request.FILES["upload"]
    title = request.POST["title"]
    album = request.POST["album"]
    artist = request.POST["artist"]
    year = request.POST["year"]
    upload_art = request.POST["upload_art"]

    data = {'song': song, 'title': title, 'album': album, 'artist': artist, 'year': year, 'upload_art': upload_art}

    id, exists = song_service.upload_song(data, request.user)

    data.pop("upload_art")
    data.pop("song")
    data["id"] = id

    return HttpResponse(content=json.dumps({"message": "exists" if exists else "success",
                                            "data": data}), status=200,
                        content_type="application/json")


@login_required
def getSongById(request, song_id):
    song_path = Song.objects.filter(id=song_id).first().song_in_bytes.file
    file_name = str(os.path.join(str(settings.MEDIA_ROOT), str(song_path)))
    logging.warning("File path: " + file_name)
    response = RangedFileResponse(request, open(file_name, 'rb'), content_type='audio/*')
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_name)}"'

    return response


@login_required
def getAlbumById(request, album_id):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for song in Song.objects.filter(album__id=album_id):
            song_path = song.song_in_bytes.file
            file_name = str(os.path.join(str(settings.MEDIA_ROOT), str(song_path)))
            with open(file_name, 'rb') as f:
                bytearray_of_song = f.read()
            zip_file.writestr(os.path.basename(file_name), io.BytesIO(bytearray_of_song).getvalue())

    response = RangedFileResponse(request, zip_buffer, content_type='application/zip')
    album_name = Album.objects.filter(id=album_id).first().name
    artist_name = Artist.objects.filter(album__id=album_id).first().name
    response['Content-Disposition'] = f'attachment; filename="{artist_name.lower()}-{album_name.lower()}.zip"'

    return response


@login_required
def getArtistById(request, artist_id):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for album in Album.objects.filter(artist__id=artist_id):
            for song in Song.objects.filter(album__id=album.id):
                song_path = song.song_in_bytes.file
                file_name = str(os.path.join(str(settings.MEDIA_ROOT), str(song_path)))
                with open(file_name, 'rb') as f:
                    bytearray_of_song = f.read()
                zip_file.writestr(f"{album.name}/{os.path.basename(file_name)}",
                                  io.BytesIO(bytearray_of_song).getvalue())

    response = RangedFileResponse(request, zip_buffer, content_type='application/zip')
    artist_name = Artist.objects.filter(id=artist_id).first().name
    response['Content-Disposition'] = f'attachment; filename="{artist_name.lower()}.zip"'

    return response


@login_required
@transaction.atomic
def deleteSong(request, song_id):
    song = Song.objects.filter(id=song_id).first()
    if not song:
        return HttpResponse(status=204)
    album = song.album
    song.delete()
    song.song_in_bytes.delete()
    show = 'song'
    if not Song.objects.filter(album__id=album.id).exists():
        albumId = album.id
        artists = Artist.objects.filter(album__id=albumId)
        album.delete()
        show = 'album'
        for artist in artists:
            if not Album.objects.filter(id=albumId, artist__id=artist.id).exists():
                show = 'artist'
                artist.delete()
    return HttpResponse(status=200, content=json.dumps({
        'show': show
    }), content_type='application/json')


@login_required
@transaction.atomic
def editSong(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id, name, album, artist = int(body["id"]), body["name"], body["album"], body["artist"]

        song = Song.objects.filter(id=id).first()
        if not song:
            return HttpResponse(status=204)
        song.name = name
        song.save()
        show = 'song'
        albums = Album.objects.filter(name=album)
        edit_album = None
        old_album = song.album

        if albums.exists():
            if song.album.id != albums.first().id:
                show = 'album'
                song.album = albums.first()
                song.save()

            edit_album = albums.first()
        else:
            record_label = None
            if not request.user.is_superuser:
                record_label = RecordLabel.objects.filter(user__id=request.user.id).first()
            new_album = copy.copy(old_album)
            new_album.id = None
            new_album.name = album
            new_album.save()

            if not request.user.is_superuser:
                record_label.album_set.add(new_album)
            song.album = new_album
            song.save()

            edit_album = new_album

        old_album_artist = Artist.objects.filter(album__id=old_album.id)
        new_album_artist = Artist.objects.filter(album__id=edit_album.id)
        new_artist = Artist.objects.filter(name=artist)

        # if old_album_artist.exists() and new_album_artist.exists() and old_album_artist.first().id != new_album_artist.first().id:
        #    old_album_artist
        # Postojao je izvođač novog albuma i novi izvođač
        if old_album_artist.exists() and new_artist.exists():
            if old_album_artist.first().id != new_artist.first().id:
                old_album_artist.first().album_set.remove(edit_album)
            new_artist.first().album_set.add(edit_album)
            edit_artist = new_artist.first()
            if not Song.objects.filter(album__id=old_album.id).exists():
                old_album.delete()
                show = 'artist'
                # if old_album_artist.exists() and not Album.objects.filter(
                #         artist__id=old_album_artist.first().id).exists():
                #     old_album_artist.first().delete()

        # Postojao je izvođač novog albuma, a nije novi izvođač
        elif old_album_artist.exists() and not new_artist.exists():
            old_album_artist.first().album_set.remove(edit_album)
            edit_artist = Artist(name=artist)
            edit_artist.save()
            edit_artist.album_set.add(edit_album)
            show = 'artist'
            if not Song.objects.filter(album__id=old_album.id).exists():
                old_album.delete()
                show = 'artist'
                # if old_album_artist.exists() and not Album.objects.filter(
                #         artist__id=old_album_artist.first.id).exists():
                #     old_album_artist.first().delete()
        # Nije postojao izvođač novog albuma, a jeste novi izvođač
        elif not old_album_artist.exists() and new_artist.exists():
            new_artist.first().album_set.add(edit_album)
            edit_artist = new_artist.first()
        # Nije postojao ni izvođač novog albuma, a ni novi izvođač
        else:
            edit_artist = Artist(name=artist)
            edit_artist.save()
            edit_artist.album_set.add(edit_album)
            show = 'artist'

        return HttpResponse(status=200, content=json.dumps({
            'id': id,
            'name': name,
            'album': album,
            'artist': artist,
            'show': show
        }), content_type='application/json')


    else:
        return HttpResponse("GET request not found.")


@login_required
@transaction.atomic
def deleteAlbum(request, album_id):
    for song in Song.objects.filter(album__id=album_id):
        song.delete()
        song.song_in_bytes.delete()
    album = Album.objects.filter(id=album_id).first()
    if not album:
        return HttpResponse(status=204)
    artists = Artist.objects.filter(album__id=album_id)
    album.delete()
    show = 'album'
    for artist in artists:
        if not Album.objects.filter(id=album_id, artist__id=artist.id).exists():
            show = 'artist'
            artist.delete()
    return HttpResponse(status=200, content=json.dumps({
        'show': show
    }), content_type='application/json')


@login_required
@transaction.atomic
def editAlbum(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id, name, artist, image_art = int(body["id"]), body["name"], body["artist"], body["imageArt"]

        show = 'song'
        edit_album = None

        old_album = Album.objects.filter(id=id).first()
        new_albums = Album.objects.filter(name=name)

        if new_albums.exists():
            if old_album.id != new_albums.first().id:
                for song in Song.objects.filter(album__id=id).all():
                    song.album = new_albums.first()
                old_album.delete()
            edit_album = new_albums.first()
        else:
            old_album.name = name
            old_album.save()

            edit_album = old_album

        old_album_artist = Artist.objects.filter(album__id=old_album.id)
        new_album_artist = Artist.objects.filter(album__id=edit_album.id)
        new_artist = Artist.objects.filter(name=artist)

        # if old_album_artist.exists() and new_album_artist.exists() and old_album_artist.first().id != new_album_artist.first().id:
        #    old_album_artist
        # Postojao je izvođač novog albuma i novi izvođač
        if old_album_artist.exists() and new_artist.exists():
            if old_album_artist.first().id != new_artist.first().id:
                old_album_artist.first().album_set.remove(edit_album)
            new_artist.first().album_set.add(edit_album)
            edit_artist = new_artist.first()
            show = 'artist'

        # Postojao je izvođač novog albuma, a nije novi izvođač
        elif old_album_artist.exists() and not new_artist.exists():
            old_album_artist.first().album_set.remove(edit_album)
            edit_artist = Artist(name=artist)
            edit_artist.save()
            edit_artist.album_set.add(edit_album)
            show = 'artist'
        # Nije postojao izvođač novog albuma, a jeste novi izvođač
        elif not old_album_artist.exists() and new_artist.exists():
            new_artist.first().album_set.add(edit_album)
            edit_artist = new_artist.first()
        # Nije postojao ni izvođač novog albuma, a ni novi izvođač
        else:
            edit_artist = Artist(name=artist)
            edit_artist.save()
            edit_artist.album_set.add(edit_album)
            show = 'artist'

        edit_album.picture = bytearray(image_art, 'utf8')
        edit_album.save()

        return HttpResponse(status=200, content=json.dumps({
            'id': id,
            'name': name,
            'artist': artist,
            'show': show
        }), content_type='application/json')


    else:
        return HttpResponse("GET request not found.")


@login_required
@transaction.atomic
def deleteArtist(request, artist_id):
    for album in Album.objects.filter(artist__id=artist_id):
        for song in Song.objects.filter(album__id=album.id):
            song.delete()
            song.song_in_bytes.delete()
        album.delete()
    artist = Artist.objects.filter(id=artist_id).first()
    artist.delete()
    return HttpResponse(status=200, content=json.dumps({
        'show': "artist"
    }), content_type='application/json')


@login_required
@transaction.atomic
def editArtist(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        id, name = int(body["id"]), body["name"]

        old_artist = Artist.objects.filter(id=id).first()
        new_artist = Artist.objects.filter(name=name)

        if new_artist.exists():
            if old_artist.id != new_artist.first().id:
                for album in Album.objects.filter(artist__id=old_artist.id).all():
                    new_artist.first().album_set.add(album)
                old_artist.album_set.clear()
        else:
            old_artist.name = name
            old_artist.save()

        return HttpResponse(status=200, content=json.dumps({
            'id': id,
            'name': name,
            'show': 'artist'
        }), content_type='application/json')


@login_required
@transaction.atomic
def editProfile(request):
    if request.method == 'POST':
        firstname, secondname, username, email, password, isUser = \
            request.POST["firstName"], request.POST["secondName"], request.POST["username"], \
            request.POST["email"], request.POST['password'], bool(strtobool(request.POST["isUser"]))

        user = request.user
        if user.check_password(password):
            user.first_name, user.last_name, user.username, user.email = firstname, secondname, username, email
            user.save()

            user_profile_info = UserProfileInfo.objects.filter(user=user)
            record_label = RecordLabel.objects.filter(user=user)
            if isUser and user_profile_info.exists():
                elem = user_profile_info.first()
                elem.picture = request.FILES['profilePicture']
                elem.save()
            elif not isUser and record_label.exists():
                elem = record_label.first()
                elem.picture = request.FILES['profilePicture']
                elem.save()
        else:
            return HttpResponse(status=204)
        return HttpResponse(status=200, content=json.dumps({
            'firstname': firstname,
            'secondname': secondname,
            'username': username,
            'email': email
        }))
    else:
        return HttpResponse(status=204)


@login_required
@transaction.atomic
def update_password(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        oldpassword, newpassword1, newpassword2 = body["oldpassword"], body["newpassword1"], body["newpassword2"]

        user = request.user
        if user.check_password(oldpassword) and newpassword1 == newpassword2:
            user.set_password(newpassword1)
            user.save()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=204)

    else:
        return HttpResponse(status=204)

@login_required
@transaction.atomic
def upload_album(request):
    pass