from django.shortcuts import render

# Create your views here.

def play_playlist(request):
    context = {

    }

    return render(request, "play_playlist.html", context)