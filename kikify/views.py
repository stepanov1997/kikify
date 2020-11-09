from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Song, Album, Artist
from ranged_fileresponse import RangedFileResponse
import stagger
import base64
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from kikify.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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
            print(f"Username: {username} and password {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'kikify/htmls/login.html', {})


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


@login_required
def home(request):
    return render(request, 'kikify/htmls/home.html')


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
