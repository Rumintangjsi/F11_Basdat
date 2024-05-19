from django.shortcuts import render
from django.db import connection as conn


def show_main(request):
    context = {
        'name': 'Kelompok',
        'class': 'Basdat F'
    }

    return render(request, "main.html", context)

def dashboard(request):
    email = request.session.get('email')
    roles = request.session.get('role')
    podcasts = []
    songs = []
    albums = []
    playlists = []

    sql = f""" SELECT 
                    nama,
                    email,
                    kota_asal,
                    gender,
                    tempat_lahir,
                    tanggal_lahir
                FROM 
                    AKUN
                WHERE 
                    email = %s
                """
    cursor = conn.cursor() 

    cursor.execute(sql, (email, ))
    results = cursor.fetchone()

    user_data = {
                'nama': results[0],
                'email': results[1],
                'kota_asal': results[2],
                'gender': "Laki-laki" if results[3] == 1 else "Perempuan",
                'tempat_lahir': results[4],
                'tanggal_lahir': results[5],
            }

    with conn.cursor() as cursor:
        if 'podcaster' in roles:
            cursor.execute("""
                SELECT k.id, k.judul 
                FROM podcast p 
                JOIN konten k ON p.id_konten = k.id 
                WHERE p.email_podcaster = %s
            """, [email])
            podcasts = cursor.fetchall()

        if 'artist' in roles or 'songwriter' in roles:
            cursor.execute("""
                SELECT k.id, k.judul 
                FROM song s 
                JOIN konten k ON s.id_konten = k.id 
                WHERE s.id_artist = (SELECT id FROM artist WHERE email_akun = %s)
            """, [email])
            songs = cursor.fetchall()

        if 'label' in roles:
            cursor.execute("""
                SELECT a.id, a.judul 
                FROM album a 
                WHERE a.id_label = (SELECT id FROM label WHERE email = %s)
            """, [email])
            albums = cursor.fetchall()

        cursor.execute("""
            SELECT up.id_user_playlist, up.judul 
            FROM user_playlist up 
            WHERE up.email_pembuat = %s
        """, [email])
        playlists = cursor.fetchall()

    context = {
        'podcasts': podcasts,
        'songs': songs,
        'albums': albums,
        'playlists': playlists,
        'user_data':user_data
    }

    return render(request, 'dashboard.html', context)