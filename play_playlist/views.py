from django.db import connection
from django.shortcuts import render

# Create your views here.

def play_playlist(request, playlist_id):
    print(playlist_id)
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

    songs = []
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
        songs = cursor.fetchall()
    songs_data = []
    for song in songs:
        data = {
            'judul': song[0],
            'tanggal_rilis': song[1],
            'tahun': song[2],
            'durasi': song[3],
            'penyanyi': song[4],
            'id': song[5]
        }
        songs_data.append(data)
    
    context = {
        'playlist': playlist_data,
        'songs': songs_data
    }
    
    return render(request, "play_playlist.html", context)