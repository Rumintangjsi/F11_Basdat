from django.shortcuts import render

# Create your views here.

def play_song(request):
    context = {

    }

    return render(request, "play_song.html", context)

def add_song_playlist(request):
    context = {

    }

    return render(request, "add_song_playlist.html", context)

def download_song(request):
    context = {

    }

    return render(request, "download_song.html", context)