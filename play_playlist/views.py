from datetime import timedelta, datetime
import json
from django.db import connection
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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
    print(f"[FOUND] {len(songs_on_playlist)} songs on playlist {playlist_id}")
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
    print(f"[FOUND] {len(all_songs)} songs")
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
    
    return render(request, "play_playlist.html", context)

@csrf_exempt
def add_song_playlist(request, playlist_id):
    if request.method == 'POST':
        song_id = request.POST.get('song-dropdown')
        # check if song is already in playlist
        with connection.cursor() as cursor:
            cursor.execute(f'''
                            SELECT * FROM PLAYLIST_SONG
                            WHERE id_playlist = '{playlist_id}' AND id_song = '{song_id}';
                        ''')
            result = cursor.fetchall()
        if len(result) > 0:
                    # get song name and playlist name
            with connection.cursor() as cursor:
                cursor.execute(f'''
                                SELECT KONTEN.judul, USER_PLAYLIST.judul
                                FROM KONTEN
                                JOIN SONG ON KONTEN.id = SONG.id_konten
                                JOIN PLAYLIST_SONG ON SONG.id_konten = PLAYLIST_SONG.id_song
                                JOIN USER_PLAYLIST ON PLAYLIST_SONG.id_playlist = USER_PLAYLIST.id_playlist
                                WHERE PLAYLIST_SONG.id_playlist = '{playlist_id}' AND PLAYLIST_SONG.id_song = '{song_id}';
                            ''')
                result2 = cursor.fetchall()
            song_name = result2[0][0]
            playlist_name = result2[0][1]
            messages.error(request, f"{song_name} is already in {playlist_name}")
            print(f"[ERROR] Song {song_id} is already in playlist {playlist_id}")
            return redirect('play_playlist:play_playlist', playlist_id=playlist_id)
        else:
            print(f"[INFO] Adding song {song_id} to playlist {playlist_id}")
        with connection.cursor() as cursor:
            e = cursor.execute(f'''
                            INSERT INTO PLAYLIST_SONG (id_playlist, id_song)
                            VALUES ('{playlist_id}', '{song_id}');
                        ''')
        if e == 1:
            print(f"[SUCCESS] Inserted song {song_id} to playlist {playlist_id}")
        else:
            print(f"[ERROR] Failed to insert song {song_id} to playlist {playlist_id}")
    else:
        print(f"[ERROR] Request method is not POST")
    return redirect('play_playlist:play_playlist', playlist_id=playlist_id)

def delete_song_playlist(request, playlist_id, song_id):
    print(f"======= [INFO] Deleting song {song_id} from playlist {playlist_id}")
    with connection.cursor() as cursor:
        cursor.execute(f'''
                       SELECT * FROM PLAYLIST_SONG;
                    ''')
        result = cursor.fetchall()
        print(f"[FOUND BFORE DELTE] {len(result)} songs on playlist")
        cursor.execute(f'''
                        DELETE 
                        FROM PLAYLIST_SONG
                        WHERE id_playlist = '{playlist_id}' AND id_song = '{song_id}';
                    ''')
        cursor.execute(f'''
                        UPDATE USER_PLAYLIST
                        SET jumlah_lagu = (
                                SELECT COUNT(*) 
                                FROM PLAYLIST_SONG 
                                WHERE id_playlist = '{playlist_id}'),
                            total_durasi = (
                                SELECT SUM(KONTEN.durasi)
                                FROM PLAYLIST_SONG
                                JOIN SONG ON SONG.id_konten = PLAYLIST_SONG.id_song
                                JOIN KONTEN ON KONTEN.id = SONG.id_konten
                                WHERE PLAYLIST_SONG.id_playlist = '{playlist_id}')
                        WHERE id_playlist = '{playlist_id}';
                    ''')
        cursor.execute(f'''
                        SELECT * FROM PLAYLIST_SONG;
                    ''')
        result = cursor.fetchall()
        print(f"[FOUND AFTER DELTE] {len(result)} songs on playlist")
    return redirect('play_playlist:play_playlist', playlist_id=playlist_id)

def shuffle_playlist(request):
    id_playlist = json.loads(request.body)['id_playlist']
    email = request.session.get('email')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    query_str = f"""SELECT * from playlist_song where id_playlist='{id_playlist}'"""
    with connection.cursor() as cursor:
        cursor.execute(query_str)
        hasil = cursor.fetchall()
    print(f"[FOUND] {len(hasil)} songs on playlist {id_playlist}")

    query_str = f"""
                SELECT id_user_playlist, email_pembuat FROM user_playlist where id_playlist='{id_playlist}'
                """
    with connection.cursor() as cursor:
        cursor.execute(query_str)
        user_playlist = cursor.fetchall()
    current_id_user_playlist = str(user_playlist[0][0])
    email_pembuat = user_playlist[0][1]
    print(f"[THIS PLAYLIST] id_user_playlist {current_id_user_playlist} by {email_pembuat}")

    query_str = f"""insert into akun_play_user_playlist (email_pembuat, id_user_playlist, email_pemain, waktu) 
                values ('{email_pembuat}', '{current_id_user_playlist}', '{email}', '{time}')"""
    with connection.cursor() as cursor:
        cursor.execute(query_str)
        print(f"[SUCCESS] Inserted user {email} to {email_pembuat} playlist's {current_id_user_playlist}")
    for a in hasil:
        id_song = str(a[1])
        query_str = f"""insert into akun_play_song (email_pemain, id_song, waktu)
                    values ('{email}', '{id_song}', '{time}')"""
        with connection.cursor() as cursor:
            cursor.execute(query_str)
            print(f"[SUCCESS] Inserted user {email} plays song with id {id_song}")
    return redirect('play_playlist:play_playlist', playlist_id=id_playlist)