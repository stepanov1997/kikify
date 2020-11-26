from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Song, Album, Artist, UserProfileInfo, ResetingPasswordQueue
from django.contrib.auth.models import User
from ranged_fileresponse import RangedFileResponse
import stagger
import base64
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from kikify.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import traceback
import secrets

MY_ADDRESS = 'XXXXXXXXXXXXXXXXXXXXXXXXXx'
PASSWORD = 'XXXXXXXXXXXXX'
SITE_ROOT = 'http://localhost:8000/kikify/'


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

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    context = {'user_form': user_form,
               'profile_form': profile_form,
               'registered': registered}

    return render(request, 'kikify/htmls/register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,
                            password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed!")
            return render(request, 'kikify/htmls/login.html', {
                'username': username
            })
    else:
        return render(request, 'kikify/htmls/login.html', {})


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
    user_profile_info = UserProfileInfo.objects.filter(user__username=request.user.username).first()
    print(user_profile_info)
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
        'about': "About"
    }
    return render(request, 'kikify/htmls/home.html', context)


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
        'artist': Artist.objects.filter(id=artist_id).first()
    }
    return render(request, 'kikify/components/albums.html', dictionary)


@login_required
def songsOfAlbum(request, artist_id, album_id):
    dictionary = {
        'songs': Song.objects.filter(album__id=album_id),
        'artist': Artist.objects.filter(id=artist_id),
        'album': Album.objects.filter(id=album_id)
    }
    print(dictionary)
    return render(request, 'kikify/components/songs.html', dictionary)


@login_required
def getSongById(request, song_id):
    song_path = Song.objects.filter(id=song_id).first().song_in_bytes.file
    response = RangedFileResponse(request, open(f"kikify/{song_path}", 'rb'), content_type='audio/*')
    response['Content-Disposition'] = f'attachment; filename="kikify/{song_path}"'
    return response
