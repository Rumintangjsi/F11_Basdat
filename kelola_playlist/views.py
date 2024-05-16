from datetime import datetime
import uuid
from django.db import connection
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

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
    
    # print(playlists_data)
    
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
    
    # print(playlists_data)
    
    context = {
        'playlists': playlists_data
    }
    
    return render(request, "playlists.html", context)

def create_playlist_page(request):
    return render(request, "create_playlist.html", {})

@csrf_exempt
def create_playlist_post(request):
    judul = ''
    deskripsi = ''
    if request.method == 'POST':
        judul = request.POST['title']
        deskripsi = request.POST['description']
        # print(f'Judul: {judul}')
        # print(f'Deskripsi: {deskripsi}')
    akun = request.session.get('akun', None)
    # print('nicole50@example.com')
    uuid1 = str(uuid.uuid4())

    query_str = f"""INSERT INTO playlist 
    VALUES ('{uuid1}')"""
    with connection.cursor() as cursor:
        e = cursor.execute(query_str)
        # print(e)

    uuid2 = str(uuid.uuid4())
    tanggal = datetime.now().strftime("%Y-%m-%d")

    query_str = f"""INSERT INTO user_playlist 
    VALUES ('nicole50@example.com', '{uuid2}', '{judul}', '{deskripsi}', '{int(0)}', '{tanggal}', '{uuid1}', '{int(0)}');"""
    with connection.cursor() as cursor:
        e = cursor.execute(query_str)
        # print(e)
    return redirect('kelola_playlist:kelola_playlist')

def delete_playlist(request, id_playlist):
    query_str = f"""DELETE FROM USER_PLAYLIST WHERE id_playlist = '{id_playlist}';"""
    with connection.cursor() as cursor:
        e = cursor.execute(query_str)
        # print(e)
    return redirect('kelola_playlist:kelola_playlist')