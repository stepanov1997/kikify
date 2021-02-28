import base64
import json
import os
import secrets
import smtplib
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, FileResponse, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from mutagen.easyid3 import EasyID3
from ranged_fileresponse import RangedFileResponse
from requests import Response

from kikify.forms import UserForm, UserProfileInfoForm
from kikify_django import settings
from . import song_service
from .models import Song, Album, RecordLabel, UserProfileInfo, ResetingPasswordQueue, Artist
from .mp3_parser import parse_tags

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


def register_record_label(request):
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

    context = {'user_form': user_form,
               'profile_form': profile_form,
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
            if RecordLabel.objects.filter(user__id=user.id).exists():
                types.append("RECORD_LABEL")

            if user.is_active and len(types) == 2:
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
                'isUser': isUser
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
                'isUser': isUser
            }
            return render(request, 'kikify/htmls/home.html', context)
        else:
            users = User.objects.filter(username=request.user.username)
            if users and len(users) > 0 and users.first() and users.first().is_superuser:
                context = {
                    'username': users.first().username,
                    'about': "About",
                    'isUser': isUser
                }
                return render(request, 'kikify/htmls/home.html', context)
            else:
                return render(request, 'kikify/htmls/login.html', {
                    'successful': False,
                    'message': 'Please log in as user.',
                    'isUser': isUser
                })
    else:
        return render(request, 'kikify/htmls/login.html', {
            'isUser': isUser
        })


@login_required
def artists(request):
    dictionary = {
        'artists': Artist.objects.all()
    }
    return render(request, 'kikify/components/artists.html', dictionary)


@login_required
def albums(request):
    dictionary = {
        'albums': Album.objects.all()
    }
    return render(request, 'kikify/components/albums.html', dictionary)


@login_required
def songs(request):
    dictionary = {
        'songs': Song.objects.all()
    }
    return render(request, 'kikify/components/songs.html', dictionary)


@login_required
def albumsOfArtist(request, artist_id):
    dictionary = {
        'albums': Album.objects.filter(artist__id=artist_id),
        'RecordLabel': RecordLabel.objects.filter(id=artist_id).first()
    }
    return render(request, 'kikify/components/albums.html', dictionary)


@login_required
def songsOfAlbum(request, artist_id, album_id):
    dictionary = {
        'songs': Song.objects.filter(album__id=album_id),
        'RecordLabel': RecordLabel.objects.filter(id=artist_id),
        'album': Album.objects.filter(id=album_id)
    }
    print(dictionary)
    return render(request, 'kikify/components/songs.html', dictionary)


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


def upload_song(request):
    song = request.FILES["upload"]
    title = request.POST["title"]
    album = request.POST["album"]
    artist = request.POST["artist"]
    year = request.POST["year"]
    upload_art = request.POST["upload_art"]

    data = {'song': song, 'title': title, 'album': album, 'artist': artist, 'year': year, 'upload_art': upload_art}

    (id, exists) = song_service.upload_song(data)

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
