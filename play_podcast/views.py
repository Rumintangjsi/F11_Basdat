from django.shortcuts import render
from django.db import connection

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def format_duration(minutes):
    hours = minutes // 60
    minutes = minutes % 60
    if hours > 0:
        return f"{hours} jam {minutes} menit"
    else:
        return f"{minutes} menit"

def play_podcast(request, id_konten):
    with connection.cursor() as cursor:
        # Fetch podcast and its podcaster details
        query_podcast = """
        SELECT k.judul, k.tanggal_rilis, k.tahun, k.durasi, a.nama as podcaster_name
        FROM podcast p
        JOIN konten k ON p.id_konten = k.id
        JOIN podcaster po ON p.email_podcaster = po.email
        JOIN akun a ON po.email = a.email
        WHERE k.id = %s;
        """
        cursor.execute(query_podcast, [id_konten])
        podcast = parse(cursor)
        
        if podcast:
            podcast = podcast[0]
            podcast['formatted_durasi'] = format_duration(podcast['durasi'])

        # Fetch episodes for the podcast
        query_episodes = """
        SELECT e.judul, e.deskripsi, e.tanggal_rilis, e.durasi
        FROM episode e
        WHERE e.id_konten_podcast = %s
        ORDER BY e.tanggal_rilis;
        """
        cursor.execute(query_episodes, [id_konten])
        episodes = parse(cursor)
        for episode in episodes:
            episode['formatted_durasi'] = format_duration(episode['durasi'])

    context = {
        'podcast': podcast,
        'episodes': episodes
    }
    return render(request, "play_podcast.html", context)
