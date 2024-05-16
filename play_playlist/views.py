from django.db import connection
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

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
    playlist_data = {
        'email_pembuat' : playlist[0], 
        'judul'         : playlist[1], 
        'deskripsi'     : playlist[2], 
        'jumlah_lagu'   : playlist[3], 
        'tanggal_dibuat': playlist[4], 
        'id_playlist'   : playlist[5], 
        'total_durasi'  : playlist[6]
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
        data = {
            'judul': song[0],
            'tanggal_rilis': song[1],
            'tahun': song[2],
            'durasi': song[3],
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