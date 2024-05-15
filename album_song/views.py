from django.shortcuts import render
import psycopg2 

conn = psycopg2.connect( 
    database="railway", 
    user='postgres', 
    password='pCIIFIIJGgOGhPBgjASGQVjzXEOYPumt', 
    host='viaduct.proxy.rlwy.net', 
    port='59310'
)

conn.autocommit = True

def album_list(request):

    albums = []

    cursor = conn.cursor() 

    # Fetch Album
    sql = """ SELECT al.id, al.judul, la.nama, al.jumlah_lagu, al.total_durasi 
              FROM album AS al 
              JOIN label AS la 
              ON la.id = al.id_label """

    cursor.execute(sql) 
    results = cursor.fetchall()

    print(results)

    for item in results:
        albums.append({
            'id': item[0],
            'title' : item[1],
            'label': item[2],
            'song_count':item[3],
            'duration': str(round(item[4]/3600)) + "hr " + str(round(item[4]%3600 / 60)) + "min"})
        
    context = {
        'albums' : albums
    }

    return render(request, "album_list.html", context)

def song_list(request, album_id):

    cursor = conn.cursor() 

    # Fetch Album Info and its songs
    sql = f""" SELECT al.id, al.judul, la.nama, al.jumlah_lagu, al.total_durasi, 
                      k.id, k.judul, ge.genre, k.durasi, s.total_play, s.total_download,
                      STRING_AGG(DISTINCT ak.nama, ',') AS artists,
                      STRING_AGG(DISTINCT ak1.nama, ',') AS songwriters
               FROM album AS al 
               JOIN label AS la ON la.id = al.id_label
               JOIN song AS s ON s.id_album = al.id
               JOIN konten AS k ON s.id_konten = k.id
               JOIN genre AS ge ON k.id = ge.id_konten

               JOIN artist AS ar ON s.id_artist = ar.id
               JOIN akun AS ak ON ar.email_akun = ak.email

               LEFT JOIN songwriter_write_song AS sws ON sws.id_song = k.id
               LEFT JOIN songwriter AS sw ON sws.id_songwriter = sw.id
               LEFT JOIN akun AS ak1 ON sw.email_akun = ak1.email

               WHERE al.id = '{album_id}'
               GROUP BY al.id, al.judul, la.nama, al.jumlah_lagu, al.total_durasi, k.id, k.judul, ge.genre, k.durasi, s.total_play, s.total_download 
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

    context = {
        'album': album,
        'songs': songs
    }

    return render(request, "song_list.html", context)

def add_song(request):
    return None

def edit_song(request, song_id):
    return None

def delete_song(request, song_id):
    return None

def add_album(request):
    return None

def edit_album(request, album_id):
    return None

def delete_album(request, album_id):
    return None
