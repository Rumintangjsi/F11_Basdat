from datetime import timedelta
from django.db import connection
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def format_duration(seconds, fmt="{:02}:{:02}:{:02}"):
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return fmt.format(hours, minutes, seconds)

def play_playlist(request, playlist_id):
    # print(playlist_id)
    playlist = {}
    with connection.cursor() as cursor:
        cursor.execute(f'''
                        SELECT email_pembuat, judul, deskripsi, jumlah_lagu, tanggal_dibuat, id_playlist, total_durasi
                        FROM USER_PLAYLIST
                        WHERE id_playlist = '{playlist_id}';
                    ''')
        playlists = cursor.fetchall()
    playlist = playlists[0]
    td = timedelta(seconds=playlist[6])
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0 & minutes > 0:
        formatted_duration = f"{hours} h {minutes} m {seconds} s"
    elif minutes > 0:
        formatted_duration = f"{minutes} m {seconds} s"
    else:
        formatted_duration = f"{seconds} s"  # Format duration as "mm:ss"
    playlist_data = {
        'email_pembuat' : playlist[0], 
        'judul'         : playlist[1], 
        'deskripsi'     : playlist[2], 
        'jumlah_lagu'   : playlist[3], 
        'tanggal_dibuat': playlist[4], 
        'id_playlist'   : playlist[5], 
        'total_durasi'  : formatted_duration
    }

    songs_on_playlist = []
    playlist_id = playlist[5]
    with connection.cursor() as cursor:
        cursor.execute(f'''
                        SELECT KONTEN.judul, KONTEN.tanggal_rilis, KONTEN.tahun, KONTEN.durasi, AKUN.nama AS penyanyi, KONTEN.id
                        FROM PLAYLIST_SONG
                        JOIN SONG ON PLAYLIST_SONG.id_song = SONG.id_konten
                        JOIN KONTEN ON SONG.id_konten = KONTEN.id
                        JOIN ARTIST ON SONG.id_artist = ARTIST.id
                        JOIN AKUN ON AKUN.email = ARTIST.email_akun
                        WHERE PLAYLIST_SONG.id_playlist = '{playlist_id}';
                    ''')
        songs_on_playlist = cursor.fetchall()
    # print(songs_on_playlist)
    songs_on_playlist_data = []
    for song in songs_on_playlist:
        td = timedelta(seconds=song[3])
        total_seconds = int(td.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0 & minutes > 0:
            formatted_duration = f"{hours} h {minutes} m {seconds} s"
        elif minutes > 0:
            formatted_duration = f"{minutes} m {seconds} s"
        else:
            formatted_duration = f"{seconds} s" 
        data = {
            'judul': song[0],
            'tanggal_rilis': song[1],
            'tahun': song[2],
            'durasi': formatted_duration,
            'penyanyi': song[4],
            'id': song[5]
        }
        songs_on_playlist_data.append(data)
    
    all_songs = []
    with connection.cursor() as cursor:
        cursor.execute(f'''
                        SELECT KONTEN.judul, KONTEN.id
                        FROM SONG
                        JOIN KONTEN ON SONG.id_konten = KONTEN.id;
                    ''')
        all_songs = cursor.fetchall()
    all_songs_data = []
    for song in all_songs:
        data = {
            'judul': song[0],
            'id_konten': str(song[1])
        }
        all_songs_data.append(data)

    context = {
        'playlist': playlist_data,
        'songs': songs_on_playlist_data,
        'all_songs': all_songs_data,
        'playlist_id': playlist_id,
    }
    # print(songs_on_playlist_data)
    # print(f'======================{all_songs_data}')
    
    return render(request, "play_playlist.html", context)

@csrf_exempt
def add_song_playlist(request, playlist_id):
    if request.method == 'POST':
        song_id = request.POST.get('song-dropdown')
        # print('=================================')
        # print(request.POST)
        # print(song_id)
        # print(playlist_id)
        # print('=================================')
    with connection.cursor() as cursor:
        cursor.execute(f'''
                        INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
                        VALUES ('{playlist_id}', '{song_id}');
                    ''')
    return redirect('play_playlist:play_playlist', playlist_id=playlist_id)

def delete_song_playlist(request, playlist_id, song_id):
    with connection.cursor() as cursor:
        cursor.execute(f'''
                        DELETE FROM PLAYLIST_SONG
                        WHERE id_playlist = '{playlist_id}' AND id_song = '{song_id}';
                    ''')
    return redirect('play_playlist:play_playlist', playlist_id=playlist_id)