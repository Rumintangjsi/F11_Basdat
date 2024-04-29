from django.shortcuts import render

def create_podcast(request):
    context = {
    }

    return render(request, "create_podcast.html", context)

def podcast_list(request):
    context = {
    }
    return render(request, "podcast_list.html", context)

def create_episode(request):
    context = {
    }
    return render(request, "create_episode.html", context)

def episode_list(request):
    context = {
    }
    return render(request, "episode_list.html", context)