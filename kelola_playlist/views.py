from django.db import connection
from django.shortcuts import render

# Create your views here.

def kelola_playlist(request):
    playlists = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT judul, email_pembuat, jumlah_lagu, total_durasi, id_playlist
                        FROM USER_PLAYLIST
                    ''')
        playlists = cursor.fetchall()
    context = {

    }
    playlists_data = []
    for playlist in playlists:
        data = {
            'judul'         : playlist[0], 
            'email_pembuat' : playlist[1], 
            'jumlah_lagu'   : playlist[2], 
            'total_durasi'  : playlist[3],
            'id_playlist'   : playlist[4]
        }
        playlists_data.append(data)
    
    print(playlists_data)
    
    context = {
        'playlists': playlists_data
    }
    
    return render(request, "playlists.html", context)

def kelola_playlist_depracated(request):
    playlists = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi
                        FROM USER_PLAYLIST
                    ''')
        playlists = cursor.fetchall()
    context = {

    }
    playlists_data = []
    for playlist in playlists:
        data = {
            'email_pembuat' : playlist[0], 
            'judul'         : playlist[1], 
            'deskripsi'     : playlist[2], 
            'jumlah_lagu'   : playlist[3], 
            'tanggal_dibuat': playlist[4], 
            'id_playlist'   : playlist[5], 
            'total_durasi'  : playlist[6]
        }
        playlists_data.append(data)
    
    print(playlists_data)
    
    context = {
        'playlists': playlists_data
    }
    
    return render(request, "playlists.html", context)

def create_playlist(request):
    context = {

    }

    return render(request, "create_playlist.html", context)