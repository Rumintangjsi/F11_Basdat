from datetime import datetime
import json
from pyexpat.errors import messages
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

# Create your views here.
def play_song(request, song_id):
    # cek akun premium
    with connection.cursor() as cursor:
        cursor.execute(f'''
                        SELECT email
                        FROM PREMIUM
                        WHERE email = '{request.session.get('email')}';
                    ''')
        result = cursor.fetchall()
    is_premium = True if (result != []) else False
    if is_premium:
        print(f"Email {request.session.get('email')} is premium")
    else:
        print(f"Email {request.session.get('email')} is not premium")
    with connection.cursor() as cursor:
        url = f'''
                SELECT judul, AKUN.nama as penyanyi, durasi, tanggal_rilis, tahun, total_play, total_download, KONTEN.id
                FROM KONTEN, SONG, AKUN, ARTIST
                WHERE KONTEN.id = SONG.id_konten 
                    AND SONG.id_artist = ARTIST.id
                    AND ARTIST.email_akun = AKUN.email
                    AND KONTEN.id = '{song_id}';
            '''
        cursor.execute(url)
        songs = cursor.fetchall()
    song = songs[0]
    song_data = {
        'judul'         : song[0], 
        'penyanyi'      : song[1], 
        'durasi'        : song[2], 
        'tanggal_rilis' : song[3], 
        'tahun'         : song[4], 
        'total_play'    : song[5], 
        'total_download': song[6],
        'id'            : str(song[7])
    }
    # genre
    with connection.cursor() as cursor:
        url = f'''
                SELECT GENRE.genre
                FROM GENRE
                WHERE GENRE.id_konten = '{song_id}';
            '''
        cursor.execute(url)
        genres = cursor.fetchall()
    genres_data = []
    print(f"[FOUND] {len(genres)} genres")
    for genre in genres:
        genres_data.append(genre[0])
    # songwriter
    with connection.cursor() as cursor:
        url = f'''
                SELECT AKUN.nama
                FROM AKUN 
                WHERE AKUN.email IN (
                    SELECT SONGWRITER.email_akun
                    FROM SONGWRITER
                    JOIN SONGWRITER_WRITE_SONG ON SONGWRITER.id = SONGWRITER_WRITE_SONG.id_songwriter
                    JOIN SONG ON SONGWRITER_WRITE_SONG.id_song = '{song_id}'
                );
            '''
        cursor.execute(url)
        songwriters = cursor.fetchall()
    print(f"[FOUND] {len(songwriters)} songwriters")
    songwriters_data = []
    for songwriter in songwriters:
        songwriters_data.append(songwriter[0])
    # album
    with connection.cursor() as cursor:
        url = f'''
                SELECT ALBUM.judul
                FROM ALBUM, SONG
                WHERE ALBUM.id = SONG.id_album
                    AND SONG.id_konten = '{song_id}';
            '''
        cursor.execute(url)
        albums = cursor.fetchall()
    albums_data = []
    for album in albums:
        albums_data.append(album[0])

    # RETRIEVE ALL USER PLAYLIST
    with connection.cursor() as cursor:
        cursor.execute(f'''
                        SELECT judul, id_playlist
                        FROM USER_PLAYLIST
                        WHERE email_pembuat = '{request.session.get('email')}';
                    ''')
        playlists = cursor.fetchall()
    playlists_data = []
    for playlist in playlists:
        data = {
            'judul': playlist[0],
            'id_playlist': playlist[1]
        }
        playlists_data.append(data)
    
    context = {
        'song': song_data,
        'songwriters': songwriters_data,
        'genres': genres_data,
        'albums': albums_data,
        'is_premium': is_premium,
        'my_playlists': playlists_data,
        'song_id': song_id,
    }

    return render(request, "play_song.html", context)

def add_song_to_playlist(request, song_id):
    if request.method == 'POST':
        playlist_id = request.POST.get('playlist-dropdown')
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
            cursor.execute(f'''
                            INSERT INTO PLAYLIST_SONG
                            VALUES ('{playlist_id}', '{song_id}');
                        ''')
        return redirect('play_playlist:play_playlist', playlist_id=playlist_id)

def songs(request):
    songs = []
    with connection.cursor() as cursor:
        cursor.execute('''
                        SELECT judul, tanggal_rilis, tahun, durasi, AKUN.nama
                        FROM KONTEN, SONG, AKUN, ARTIST
                        WHERE KONTEN.id = SONG.id_konten 
                            AND SONG.id_artist = ARTIST.id
                            AND ARTIST.email_akun = AKUN.email
                    ''')
        songs = cursor.fetchall()
    songs_data = []
    for song in songs:
        data = {
            'judul': song[0],
            'tanggal_rilis': song[1],
            'tahun': song[2],
            'durasi': song[3],
            'penyanyi': song[4]
        }
        songs_data.append(data)

    # print(songs_data)
    return render(request, "songs.html", {"songs": songs_data})

@csrf_exempt
def song_played(request):
    email = request.session.get('email')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    song_id = json.loads(request.body)['id_song']

    print(f'User with email {email} played song with id {song_id} at {time}')

    # update total play
    with connection.cursor() as cursor:
        print("Increment total play...")
        cursor.execute(f'''
                        UPDATE SONG
                        SET total_play = total_play + 1
                        WHERE id_konten = '{song_id}';
                    ''')
        print("Increment total play success")
        result = cursor.rowcount

    with connection.cursor() as cursor:
        print("Adding song to user's play history...")
        cursor.execute(f'''
                        INSERT INTO
                        AKUN_PLAY_SONG
                        VALUES ('{email}', '{song_id}', '{time}');
                    ''')
        print("Adding song to user's play history success")
        result_2 = cursor.rowcount
    if result:
        if result_2:
            return redirect('play_song:play_song', song_id=song_id)
        else:
            return HttpResponse('Berhasil memainkan lagu', status=200)
    else:
        return HttpResponse('Gagal memainkan lagu', status=400)
    

@csrf_exempt
def handle_download(request):
    email = request.session.get('email')
    id = json.loads(request.body)['id_song']

    query_str = f"""INSERT INTO downloaded_song VALUES ( '{id}', '{email}')"""
    print("Adding song with id " + id + " to download history of user with email " + email + "...")
    try:
        with connection.cursor() as cursor:
            hasil = cursor.execute(query_str)
        print("[SUCCESS] Status keberhasilan download: " + str(hasil == None))
        return HttpResponse('berhasil')
    except Exception as e:
        print("[FAILED] download")
        print("Adding song to download history failed")
        return HttpResponseServerError('gagal')