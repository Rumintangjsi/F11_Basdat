from django.shortcuts import render

# Create your views here.
def search_bar(request):
    context = {
    }
    return render(request, "search_bar.html", context)

def song_details(request):
    context = {
    }
    return render(request, "song_details.html", context)