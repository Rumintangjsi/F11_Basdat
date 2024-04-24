from django.shortcuts import render

def play_podcast(request):
    context = {
        'name': 'Kelompok',
        'class': 'Basdat F'
    }

    return render(request, "play_podcast.html", context)