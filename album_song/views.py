import json
import uuid
from django.http import JsonResponse
from django.shortcuts import render
import psycopg2

from django.db import connection as conn

def album_list(request):

    email = request.session['email']
    roles = request.session['role']

    context = {
        'email' : email,
        'roles' : roles
    }
    
    if ('artist' in roles) or ('songwriter' in roles):
        return render(request, "album_list.html", context)
    else:
        return render(request, "album_list.html", {'message': 'You cant access album dashboard'})

def song_list(request, album_id):
    context = {
        'album_id' : album_id
    }
    return render(request, "song_list.html", context)

def fetch_album(request):
    albums = []

    cursor = conn.cursor() 
   
    sql = """ SELECT al.id, al.judul, la.nama, al.jumlah_lagu, al.total_durasi 
                FROM album AS al 
                JOIN label AS la 
                ON la.id = al.id_label """
    cursor.execute(sql)
    results = cursor.fetchall()
    
    for item in results:
        albums.append({
            'id': item[0],
            'title': item[1],
            'label': item[2],
            'song_count': item[3],
            'duration': f"{item[4]//3600}hr {item[4]%3600//60}min"
        })

    sql = """ SELECT id, nama FROM label """
    cursor.execute(sql)
    labels = cursor.fetchall()

    response = {
        'albums': albums,
        'labels' : labels,
    }

    return JsonResponse(response)

def fetch_song(request):

    album_id = request.GET.get('album_id')

    cursor = conn.cursor() 

    sql = f""" SELECT a.id, a.judul, l.nama, jumlah_lagu, a.total_durasi, 
                    k.id, k.judul, g.genre, k.durasi, s.total_play, s.total_download,
                    STRING_AGG(DISTINCT ak.nama, ',') AS artists,
                    STRING_AGG(DISTINCT ak1.nama, ',') AS songwriters
            FROM album AS a 
            JOIN label AS l ON l.id = a.id_label
            JOIN song AS s ON s.id_album = a.id
            JOIN konten AS k ON s.id_konten = k.id
            JOIN genre AS g ON k.id = g.id_konten

            JOIN artist AS ar ON s.id_artist = ar.id
            JOIN akun AS ak ON ar.email_akun = ak.email

            LEFT JOIN songwriter_write_song AS sws ON sws.id_song = k.id
            LEFT JOIN songwriter AS sw ON sws.id_songwriter = sw.id
            LEFT JOIN akun AS ak1 ON sw.email_akun = ak1.email

            WHERE a.id = '{album_id}'
            GROUP BY a.id, a.judul, l.nama, a.jumlah_lagu, a.total_durasi, k.id, k.judul, g.genre, k.durasi, s.total_play, s.total_download 
            ORDER BY k.tanggal_rilis ASC """

    cursor.execute(sql) 
    results = cursor.fetchall()


    album_info = results[0][:5]
    album = {
        'id': album_info[0],
        'title': album_info[1],
        'label': album_info[2],
        'song_count': album_info[3],
        'duration': f"{round(album_info[4]/3600)}hr {round((album_info[4]%3600)/60)}min"
    }

    songs = []
    for row in results:
        artists = row[11].split(',') if row[11] else []
        songwriters = row[12].split(',') if row[12] else []

        songs.append({
            'id': row[5],
            'title': row[6],
            'artist': artists[0],
            'songwriters': songwriters,
            'genre': row[7],
            'duration': f"{round(row[8]/60)}:{round(row[8]%60)}",
            'plays': row[9],
            'downloads': row[10]
        })

    return JsonResponse({
        'album': album,
        'songs': songs
    })

def add_album(request):

    if request.method == 'POST':
        form_data = json.loads(request.body)
        judul = form_data.get('title')
        id_label = form_data.get('label')

        id = uuid.uuid4()
        jumlah_lagu = 0
        total_durasi = 0

        cursor = conn.cursor() 
        
        sql = f""" 
            INSERT INTO album (id, judul, jumlah_lagu, id_label, total_durasi) 
            VALUES (%s, %s, %s, %s, %s)
            """
        
        cursor.execute(sql, (id, judul, jumlah_lagu, id_label, total_durasi))
        conn.commit()

        return JsonResponse({'message': 'Album created successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def edit_album(request, album_id):
    return None

def delete_album(request, album_id):
    
    if request.method == 'DELETE':

        cursor = conn.cursor() 
        sql = """ DELETE FROM album WHERE id = %s """
        cursor.execute(sql, (album_id,))
        conn.commit()

        return JsonResponse({'message': 'Album deleted successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def add_song(request):
    return None

def edit_song(request, song_id):
    return None

def delete_song(request, song_id):
    return None