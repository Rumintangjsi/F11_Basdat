from datetime import datetime
import uuid
from django.db import connection
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def kelola_playlist(request):
    playlists = []
    email_pembuat = request.session.get('email', None)
    with connection.cursor() as cursor:
        cursor.execute(f'''
                        SELECT judul, email_pembuat, jumlah_lagu, total_durasi, id_playlist
                        FROM USER_PLAYLIST
                        WHERE email_pembuat = '{email_pembuat}';
                    ''')
        playlists = cursor.fetchall()
    context = {

    }
    playlists_data = []
    for playlist in playlists:
        seconds = playlist[3]
        print(f"[INFO] length: {seconds} in seconds")
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0 & minutes > 0:
            formatted_duration = f"{hours} h {minutes} m {seconds} s"
        elif minutes > 0:
            formatted_duration = f"{minutes} m {seconds} s"
        else:
            formatted_duration = f"{seconds} s"
        data = {
            'judul'         : playlist[0], 
            'email_pembuat' : playlist[1], 
            'jumlah_lagu'   : playlist[2], 
            'total_durasi'  : formatted_duration,
            'id_playlist'   : playlist[4]
        }
        print(f"[INFO] length: {formatted_duration}")
        playlists_data.append(data)
    
    print(f"[FOUND] {len(playlists_data)} playlists")
    
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
    akun = request.session.get('akun', None)
    uuid1 = str(uuid.uuid4())

    query_str = f"""INSERT INTO playlist 
    VALUES ('{uuid1}')"""
    with connection.cursor() as cursor:
        e = cursor.execute(query_str)
        print("==================================")
        print(f"ERROR MESSAGE: {e}")

    email = request.session.get('email', None)
    uuid2 = str(uuid.uuid4())
    tanggal = datetime.now().strftime("%Y-%m-%d")

    query_str = f"""INSERT INTO user_playlist 
    VALUES ('{email}', '{uuid2}', '{judul}', '{deskripsi}', '{int(0)}', '{tanggal}', '{uuid1}', '{int(0)}');"""
    with connection.cursor() as cursor:
        e = cursor.execute(query_str)
    return redirect('kelola_playlist:kelola_playlist')

def delete_playlist(request, id_playlist):
    query_str = f"""DELETE FROM USER_PLAYLIST WHERE id_playlist = '{id_playlist}';"""
    with connection.cursor() as cursor:
        e = cursor.execute(query_str)
        # print(e)
    return redirect('kelola_playlist:kelola_playlist')

def edit_playlist_page(request, id_playlist):
    print(id_playlist)
    playlist = []
    url = f'''SELECT judul, deskripsi
                FROM USER_PLAYLIST
                WHERE id_playlist = '{id_playlist}';
                '''
    with connection.cursor() as cursor:
        cursor.execute(url)
        playlist = cursor.fetchall()
    context = {
        'id_playlist': id_playlist,
        'judul': playlist[0][0],
        'deskripsi': playlist[0][1]
    }
    return render(request, "edit_playlist.html", context)

def edit_playlist_post(request, id_playlist):
    print(id_playlist)
    judul = ''
    deskripsi = ''
    if request.method == 'POST':
        judul = request.POST['title']
        deskripsi = request.POST['description']
        # print(f'Judul: {judul}')
        # print(f'Deskripsi: {deskripsi}')
    query_str = f"""UPDATE USER_PLAYLIST 
                    SET judul = '{judul}', deskripsi = '{deskripsi}' 
                    WHERE id_playlist = '{id_playlist}';"""
    with connection.cursor() as cursor:
        e = cursor.execute(query_str)
    if isinstance(e, int):
        print('[SUCCESS] Playlist updated')
    else:
        print('[ERROR] Playlist not updated')
    return redirect('kelola_playlist:kelola_playlist')