import uuid
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.db import connection
from django.urls import reverse
from .query import get_konten
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

def create_podcast(request, email_podcaster):
    cursor = connection.cursor()

    if request.method == 'POST':
        judul = request.POST.get('judul')
        genre = request.POST.get('genre')
        durasi = request.POST.get('durasi')

        new_uuid = str(uuid.uuid4())
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime('%Y-%m-%d')
        current_year = current_datetime.year

        cursor.execute(f"""
            INSERT INTO KONTEN 
            VALUES ('{new_uuid}', '{judul}', '{formatted_date}', '{current_year}', '{durasi}');
        """)

        cursor.execute(f"""
            INSERT INTO GENRE VALUES 
            ('{new_uuid}', '{genre}');
        """)

        cursor.execute(f"""
            INSERT INTO PODCAST  VALUES 
            ('{new_uuid}', '{email_podcaster}');
        """)

        cursor.execute(f"""
            SELECT KONTEN.judul, GENRE.genre, KONTEN.durasi 
            FROM KONTEN, GENRE 
            WHERE KONTEN.id='{new_uuid}' AND GENRE.id_konten=KONTEN.id;
        """)
        create_result = cursor.fetchone()

        
        context = {
            'judul': create_result[0],
            'genre': create_result[1],
            'durasi': create_result[2],
            'error': None
        }
        return redirect('kelola_podcast:podcast_list')
    else:
        return render(request, "create_podcast.html")

def parse(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def podcast_list(request, email_podcaster):
    context = {}

    with connection.cursor() as cursor:
        query = """
        SELECT p.id_konten, k.judul, k.tahun, COUNT(e.id_episode) as episode_count, COALESCE(SUM(e.durasi), 0) as total_duration
        FROM podcast p
        JOIN konten k ON p.id_konten = k.id
        LEFT JOIN episode e ON k.id = e.id_konten_podcast
        WHERE p.email_podcaster = %s
        GROUP BY p.id_konten, k.judul, k.tahun
        ORDER BY k.judul;
        """
        cursor.execute(query, [email_podcaster])
        podcasts = parse(cursor)
        context["podcasts"] = podcasts

        if podcasts:
            # Collect all content IDs from podcasts in a single query
            content_ids = [podcast['id_konten'] for podcast in podcasts]
            placeholders = ', '.join(['%s'] * len(content_ids))
            content_query = f"SELECT * FROM konten WHERE id IN ({placeholders});"
            
            cursor.execute(content_query, content_ids)
            all_contents = parse(cursor)
            
            # Map contents back to their respective podcasts
            content_dict = {content['id']: content for content in all_contents}
            for podcast in podcasts:
                podcast['contents'] = content_dict.get(podcast['id_konten'], [])
                
        print(context)
        return render(request, "podcast_list.html", context)

@csrf_exempt
def create_episode(request, id_konten):
    context = {'id_konten':id_konten}
    with connection.cursor() as cursor:
        cursor.execute("SELECT judul FROM konten WHERE id = %s", [id_konten])
        podcast = cursor.fetchone()  # Fetches the first row of the query results
        
        # Check if the podcast exists
        if podcast:
            context['podcast_judul'] = podcast[0]  # Store the title in the context
        else:
            # Handle the case where no podcast is found
            context['podcast_judul'] = "No podcast found"
    if request.method == 'POST':
        judul_episode = request.POST.get('judul_episode')
        deskripsi = request.POST.get('deskripsi')
        durasi = int(request.POST.get('durasi'))
        id_episode = str(uuid.uuid4())
        tanggal = datetime.now().strftime("%Y-%m-%d")
        tahun = datetime.now().year

        # Insert data into episode 
        create_episode_query = f"""
            INSERT INTO episode
            VALUES ('{id_episode}', '{id_konten}', '{judul_episode}', '{deskripsi}', '{durasi}', '{tanggal}');
            """
        print(f'query:{create_episode_query}')
        with connection.cursor() as cursor:
            f = cursor.execute(create_episode_query)
        
        return redirect('kelola_podcast:podcast_list')
    else:
        return render(request, "create_episode.html", context)

def episode_list(request, podcast_id):
    context = {}
    
    # Fetch podcast details along with the author's name
    with connection.cursor() as cursor:
        query = """
        SELECT k.judul, a.nama AS author_name
        FROM konten k
        JOIN podcast p ON k.id = p.id_konten
        JOIN akun a ON p.email_podcaster = a.email
        WHERE k.id = %s;
        """
        cursor.execute(query, [podcast_id])
        podcast = cursor.fetchone()  # Fetches the first row of the query results
        
        # Check if the podcast exists
        if podcast:
            context['podcast_judul'] = podcast[0]  # Store the title in the context
            context['author_name'] = podcast[1]    # Store the author's name in the context
        else:
            # Handle the case where no podcast is found
            context['podcast_judul'] = "No podcast found"
            context['author_name'] = "Unknown author"
    
    # Fetch the podcast object itself
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM podcast WHERE id_konten = %s", [podcast_id])
        context['podcast'] = parse(cursor)[0]  # Assuming you fetch only one podcast

    # Fetch episodes for the podcast
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM episode WHERE id_konten_podcast = %s ORDER BY tanggal_rilis DESC", [podcast_id])
        context['episodes'] = parse(cursor)

    return render(request, "episode_list.html", context)

def delete_episode(request, episode_id):
    cursor = connection.cursor()

    cursor.execute(f"""
                SELECT id_konten_podcast
                FROM EPISODE
                WHERE id_episode = '{episode_id}';
            """)
    results = cursor.fetchall()

    cursor.execute(f"""
                DELETE
                FROM EPISODE
                WHERE id_episode = '{episode_id}';
            """)
    
    return redirect(reverse('kelola_podcast:episode_list', args=[str(results[0][0])]))

def delete_podcast(request, podcast_id):
    with connection.cursor() as cursor:
        # Find all episodes associated with the podcast
        cursor.execute("""
            SELECT id_episode
            FROM episode
            WHERE id_konten_podcast = %s;
        """, [podcast_id])
        episodes = cursor.fetchall()

        # Delete all episodes associated with the podcast
        for episode in episodes:
            cursor.execute("""
                DELETE
                FROM episode
                WHERE id_episode = %s;
            """, [episode[0]])

        # Delete the podcast itself
        cursor.execute("""
            DELETE FROM podcast
            WHERE id_konten = %s;
        """, [podcast_id])

        # Optionally delete the content associated with the podcast
        cursor.execute("""
            DELETE FROM konten
            WHERE id = %s;
        """, [podcast_id])

    return redirect('kelola_podcast:podcast_list')
