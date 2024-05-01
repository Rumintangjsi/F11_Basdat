from django.shortcuts import render

def album_list(request):
    context = {
        'albums' : [
            {
                'title' : "1989",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            },
            {
                'title' : "The Tortured Poets Department",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            },
            {
                'title' : "The Tortured Poets Department",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            },
            {
                'title' : "The Tortured Poets Department",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            },
            {
                'title' : "The Tortured Poets Department",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            },
            {
                'title' : "The Tortured Poets Department",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            },
            {
                'title' : "The Tortured Poets Department",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            },
            {
                'title' : "The Tortured Poets Department",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            },
            {
                'title' : "The Tortured Poets Department",
                'label' : "Republic Records",
                'song_count' : 31,
                "duration" : "2 hr 2 m",
            }
        ]
    }

    return render(request, "album_list.html", context)

def song_list(request, album_id):
    context = {}
    
    return render(request, "song_list.html", context)

def add_song(request):
    return None

def edit_song(request, song_id):
    return None

def delete_song(request, song_id):
    return None

def add_album(request):
    return None

def edit_album(request, album_id):
    return None

def delete_album(request, album_id):
    return None
