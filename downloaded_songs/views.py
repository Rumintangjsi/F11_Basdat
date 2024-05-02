from django.shortcuts import render

# Create your views here.
def downloaded_songs(request):
    context = {
    }
    return render(request, "downloaded_songs.html", context)