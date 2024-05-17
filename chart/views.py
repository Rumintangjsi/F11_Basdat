from django.shortcuts import render
from django.db import connection

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def chart(request):
    with connection.cursor() as cursor:
        query = """
        SELECT pl.id AS id_playlist, ch.tipe, count(pl.id) as playlist_count
        FROM playlist pl
        JOIN chart ch ON pl.id = ch.id_playlist
        GROUP BY pl.id, ch.tipe
        ORDER BY playlist_count DESC;
        """
        cursor.execute(query)
        chart_items = parse(cursor)

    context = {
        'chart_items': chart_items
    }
    return render(request, "chart.html", context)


def chart_detail(request, id_playlist):
    context = {'id_playlist': id_playlist}
    with connection.cursor() as cursor:
        # Fetch the chart type
        cursor.execute("SELECT tipe FROM chart WHERE id_playlist = %s", [id_playlist])
        chart = cursor.fetchone()  # Fetches the first row of the query results
        
        if chart:
            context['chart_type'] = chart[0]  # Correctly referencing the first column
        else:
            context['chart_type'] = "No chart found"

        # Fetch the songs based on the playlist
        # query = """
        # SELECT s.id_konten, k.judul as song_title, a.nama as artist_name, k.tanggal_rilis, s.total_play
        # FROM song s
        # JOIN konten k ON s.id_konten = k.id
        # JOIN artist ar ON s.id_artist = ar.id
        # JOIN akun a ON ar.email_akun = a.email
        # JOIN playlist_song ps ON ps.id_song = s.id_konten
        # WHERE ps.id_playlist = %s AND
        #       k.tanggal_rilis >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month') AND
        #       k.tanggal_rilis < DATE_TRUNC('month', CURRENT_DATE)
        # ORDER BY s.total_play DESC
        # LIMIT 20;
        # """

        query = """
        SELECT s.id_konten, k.judul AS song_title, a.nama AS artist_name, k.tanggal_rilis, s.total_play
        FROM song s
        JOIN konten k ON s.id_konten = k.id
        JOIN artist ar ON s.id_artist = ar.id
        JOIN akun a ON ar.email_akun = a.email
        JOIN playlist_song ps ON ps.id_song = s.id_konten
        WHERE ps.id_playlist = %s
        ORDER BY s.total_play DESC
        LIMIT 20;
        """
        cursor.execute(query, [id_playlist])
        songs = parse(cursor)

    context['songs'] = songs
    return render(request, "chart_detail.html", context)