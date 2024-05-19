import json
import uuid
from django.http import JsonResponse
from django.shortcuts import render
from datetime import datetime

from django.db import connection as conn

def album_list(request):

    email = request.session['email']
    roles = request.session['role']

    print(roles)

    if 'artist' in roles:
        sql = f""" SELECT nama, id FROM akun JOIN artist ON akun.email = artist.email_akun WHERE akun.email = %s"""
        cursor = conn.cursor() 

        cursor.execute(sql, (email, ))
        results = cursor.fetchone()
        nama = results[0]
        id = results[1]

    if 'songwriter' in roles:
        sql = f""" SELECT nama, id FROM akun JOIN songwriter ON akun.email = songwriter.email_akun WHERE akun.email = %s"""
        cursor = conn.cursor() 

        cursor.execute(sql, (email, ))
        results = cursor.fetchone()
        nama = results[0]
        id = results[1]
    
    if 'label' in roles:
        sql = f""" SELECT nama, id FROM label WHERE email = %s"""
        cursor = conn.cursor() 

        cursor.execute(sql, (email, ))
        results = cursor.fetchone()
        nama = results[0]
        id = results[1]
    
    context = {
        'id' : id,
        'nama' : nama,
        'email' : email,
        'roles' : roles
    }
    
    if ('artist' in roles) or ('songwriter' in roles):
        return render(request, "album_list.html", context)
    else:
        return render(request, "album_list.html", {'message': 'You can\'t access album dashboard'})

def song_list(request, album_id):

    email = request.session['email']
    roles = request.session['role']

    if 'artist' in roles:
        sql = f""" SELECT nama, id FROM akun JOIN artist ON akun.email = artist.email_akun WHERE akun.email = %s"""
        cursor = conn.cursor() 

        cursor.execute(sql, (email, ))
        results = cursor.fetchone()
        nama = results[0]
        id = results[1]

    if 'songwriter' in roles:
        sql = f""" SELECT nama, id FROM akun JOIN songwriter ON akun.email = songwriter.email_akun WHERE akun.email = %s"""
        cursor = conn.cursor() 

        cursor.execute(sql, (email, ))
        results = cursor.fetchone()
        nama = results[0]
        id = results[1]
    
    context = {
        'id' : id,
        'nama' : nama,
        'email' : email,
        'roles' : roles,
        'album_id' : album_id
    }
    
    if ('artist' in roles) or ('songwriter' in roles):
        return render(request, "song_list.html", context)
    else:
        return render(request, "song_list.html", {'message': 'You can\'t access album dashboard'})
        
def fetch_album(request):
    albums = []

    email = request.session['email']
    roles = request.session['role']

    if ('artist' in roles):
        cursor = conn.cursor() 
    
        sql = """ SELECT DISTINCT
                    AL.id AS album_id,
                    AL.judul AS album_title,
                    LA.nama AS label_name,
                    AL.jumlah_lagu AS song_count,
                    AL.total_durasi AS total_duration
                FROM 
                    ALBUM AL
                    JOIN LABEL LA ON AL.id_label = LA.id
                    JOIN SONG S ON AL.id = S.id_album
                    JOIN ARTIST AR ON S.id_artist = AR.id
                    JOIN AKUN A ON AR.email_akun = A.email
                WHERE 
                    A.email = %s
                """
        
        cursor.execute(sql, (email, ))
        results = cursor.fetchall()
    
        for item in results:
            albums.append({
                'id': item[0],
                'title': item[1],
                'label': item[2],
                'song_count': item[3],
                'duration': f"{round(item[4]/3600)}hr {round((item[4]%3600)/60)}min"
            })
    
    if ('songwriter' in roles):
        cursor = conn.cursor() 
    
        sql = """ SELECT DISTINCT
                    AL.id AS album_id,
                    AL.judul AS album_title,
                    LA.nama AS label_name,
                    AL.jumlah_lagu AS song_count,
                    AL.total_durasi AS total_duration
                FROM 
                    ALBUM AL
                    JOIN LABEL LA ON AL.id_label = LA.id
                    JOIN SONG S ON AL.id = S.id_album
                    JOIN SONGWRITER_WRITE_SONG SWS ON S.id_konten = SWS.id_song
                    JOIN SONGWRITER SW ON SWS.id_songwriter = SW.id
                    JOIN AKUN A ON SW.email_akun = A.email
                WHERE 
                    A.email = %s
                """
        
        cursor.execute(sql, (email, ))
        results = cursor.fetchall()
    
        for item in results:
            albums.append({
                'id': item[0],
                'title': item[1],
                'label': item[2],
                'song_count': item[3],
                'duration': f"{round(item[4]/3600)}hr {round((item[4]%3600)/60)}min"
            })

    sql = """ SELECT id, nama FROM label """
    cursor.execute(sql)
    labels = cursor.fetchall()

    sql = """ SELECT DISTINCT genre FROM genre """
    cursor.execute(sql)
    genres = cursor.fetchall()

    sql = """ SELECT id, nama FROM artist JOIN akun on email_akun = email """
    cursor.execute(sql)
    artists = cursor.fetchall()

    sql = """ SELECT id, nama FROM songwriter JOIN akun on email_akun = email """
    cursor.execute(sql)
    songwriters = cursor.fetchall()

    response = {
        'albums': albums,
        'genres' : genres,
        'labels' : labels,
        'artists' : artists,
        'songwriters' : songwriters
    }

    return JsonResponse(response)

def fetch_song(request):

    album_id = request.GET.get('album_id')
    email = request.session['email']

    cursor = conn.cursor() 

    sql = """ SELECT 
                AL.id AS album_id,
                AL.judul AS album_title,
                LA.nama AS label_name,
                COALESCE(AL.jumlah_lagu, 0) AS song_count,
                COALESCE(AL.total_durasi, 0) AS total_duration
            FROM 
                ALBUM AL
                JOIN LABEL LA ON AL.id_label = LA.id
                LEFT JOIN SONG S ON AL.id = S.id_album
                LEFT JOIN ARTIST AR ON S.id_artist = AR.id
            WHERE 
                AL.id = %s; """

    cursor.execute(sql, (album_id, )) 
    results = cursor.fetchall()

    album_info = results[0]
    album = {
        'id': album_info[0],
        'title': album_info[1],
        'label': album_info[2],
        'song_count': album_info[3],
        'duration': f"{round(album_info[4]/3600)}hr {round((album_info[4]%3600)/60)}min"
    }

    sql = f""" SELECT 
                    k.id AS song_id,
                    k.judul AS song_title,
                    COALESCE(STRING_AGG(DISTINCT g.genre, ','), '') AS genres,
                    k.durasi AS song_duration,
                    s.total_play AS total_plays,
                    s.total_download AS total_downloads,
                    ak.nama AS artist_name,
                    ak.email AS artist_email,
                    COALESCE(STRING_AGG(DISTINCT ak1.nama, ','), '') AS songwriter_names,
                    COALESCE(STRING_AGG(DISTINCT ak1.email, ','), '') AS songwriter_emails
                FROM 
                    song AS s
                JOIN 
                    konten AS k ON s.id_konten = k.id
                JOIN 
                    artist AS ar ON s.id_artist = ar.id
                JOIN 
                    akun AS ak ON ar.email_akun = ak.email
                LEFT JOIN 
                    genre AS g ON k.id = g.id_konten
                LEFT JOIN 
                    songwriter_write_song AS sws ON sws.id_song = k.id
                LEFT JOIN 
                    songwriter AS sw ON sws.id_songwriter = sw.id
                LEFT JOIN 
                    akun AS ak1 ON sw.email_akun = ak1.email
                WHERE 
                    s.id_album = %s
                GROUP BY 
                    k.id, k.judul, k.durasi, 
                    s.total_play, s.total_download, 
                    ak.nama, ak.email;


            """

    cursor.execute(sql, (album_id, )) 
    results = cursor.fetchall()

    songs = []
    for row in results:
        songs.append({
            'id': row[0],
            'title': row[1],
            'genre': row[2],
            'duration': f"{round(row[3]/60)}:{round(row[3]%60)}",
            'plays': row[4],
            'downloads': row[5],
            'artist': row[6],
            'artist_email': row[7],
            'songwriter': row[8],
            'songwriter_email': row[9]
        })
    
    sql = """ SELECT DISTINCT genre FROM genre """
    cursor.execute(sql)
    genres = cursor.fetchall()

    sql = """ SELECT id, nama FROM artist JOIN akun on email_akun = email """
    cursor.execute(sql)
    artists = cursor.fetchall()

    sql = """ SELECT id, nama FROM songwriter JOIN akun on email_akun = email """
    cursor.execute(sql)
    songwriters = cursor.fetchall()

    return JsonResponse({
        'user_email': email,
        'album': album,
        'songs': songs,
        'genres': genres,
        'artists' : artists,
        'songwriters' : songwriters
    })

def add_album(request):

    if request.method == 'POST':
        form_data = json.loads(request.body)
        judul = form_data.get('title')
        id_label = form_data.get('label')

        judul_lagu = form_data.get('judul_lagu')
        artist = form_data.get('artist')
        songwriter = form_data.get('songwriter')
        genre = form_data.get('genre')
        durasi = form_data.get('durasi')

        album_id = uuid.uuid4()
        jumlah_lagu = 0
        total_durasi = 0
        
        cursor = conn.cursor() 
        
        sql = f""" 
            INSERT INTO album (id, judul, jumlah_lagu, id_label, total_durasi) 
            VALUES (%s, %s, %s, %s, %s)
            """
        
        cursor.execute(sql, (album_id, judul, jumlah_lagu, id_label, total_durasi))
        conn.commit()

        konten_id = uuid.uuid4()
        current_date = datetime.now().date()
        current_year = datetime.now().year

        sql = f"""
            INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi) 
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (konten_id, judul_lagu, current_date, current_year, durasi))
        conn.commit()

        sql = f"""
            INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download) 
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (konten_id, artist, album_id, 0, 0))
        conn.commit()

        # TODO multiple genre

        sql = f"""
            INSERT INTO genre (id_konten, genre) 
            VALUES (%s, %s)
        """

        cursor.execute(sql, (konten_id, genre))
        conn.commit()

        # TODO multiple songwriter

        sql = f"""
            INSERT INTO songwriter_write_song (id_songwriter, id_song) 
            VALUES (%s, %s)
        """

        cursor.execute(sql, (songwriter, konten_id))
        conn.commit()

        return JsonResponse({'message': 'Album created successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

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
    if request.method == 'POST':

        form_data = json.loads(request.body)

        judul_lagu = form_data.get('judul_lagu')
        artist = form_data.get('artist')
        songwriter = form_data.get('songwriter')
        genre = form_data.get('genre')
        durasi = form_data.get('durasi')
        album = form_data.get('album')
                
        cursor = conn.cursor() 

        konten_id = uuid.uuid4()
        current_date = datetime.now().date()
        current_year = datetime.now().year

        sql = f"""
            INSERT INTO konten (id, judul, tanggal_rilis, tahun, durasi) 
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (konten_id, judul_lagu, current_date, current_year, durasi))
        conn.commit()

        sql = f"""
            INSERT INTO song (id_konten, id_artist, id_album, total_play, total_download) 
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (konten_id, artist, album, 0, 0))
        conn.commit()

        sql = f"""
            INSERT INTO genre (id_konten, genre) 
            VALUES (%s, %s)
        """

        cursor.execute(sql, (konten_id, genre))
        conn.commit()

        sql = f"""
            INSERT INTO songwriter_write_song (id_songwriter, id_song) 
            VALUES (%s, %s)
        """

        cursor.execute(sql, (songwriter, konten_id))
        conn.commit()
    
        return JsonResponse({'message': 'Song created successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def delete_song(request, konten_id):

    if request.method == 'DELETE':

        cursor = conn.cursor() 
        sql = f""" DELETE FROM song WHERE id_konten = %s """
        cursor.execute(sql, (konten_id,))

        cursor = conn.cursor() 
        sql = f""" DELETE FROM konten WHERE id = %s """
        cursor.execute(sql, (konten_id,))
        conn.commit()

        return JsonResponse({'message': 'Song deleted successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)