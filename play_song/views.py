import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.

def play_song(request, song_id):
    print(song_id)
    with connection.cursor() as cursor:
        url = f'''
                SELECT judul, AKUN.nama as penyanyi, durasi, tanggal_rilis, tahun, total_play, total_download
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
        'total_download': song[6]
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
    
    context = {
        'song': song_data,
        'songwriters': songwriters_data,
        'genres': genres_data,
        'albums': albums_data
    }

    return render(request, "play_song.html", context)

def add_song_playlist(request):
    context = {

    }

    return render(request, "add_song_playlist.html", context)

def download_song(request):
    context = {

    }

    return render(request, "download_song.html", context)

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

    print(songs_data)
    return render(request, "songs.html", {"songs": songs_data})