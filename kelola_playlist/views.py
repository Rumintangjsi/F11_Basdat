from django.shortcuts import render

# Create your views here.

def kelola_playlist(request):
    context = {

    }

    return render(request, "playlists.html", context)

def create_playlist(request):
    context = {

    }

    return render(request, "create_playlist.html", context)