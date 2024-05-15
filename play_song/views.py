import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection

# Create your views here.

def play_song(request):
    context = {

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