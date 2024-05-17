import json
from django.http import JsonResponse
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

def search(request):
    context={}
    return render(request, 'search_bar.html', context)

# Create your views here.
def search_bar_songs(request):
    
    form_data = json.loads(request.body)
    song = form_data.get('song')
    
    print(form_data)
    songs = []

    
    try:
        cursor = conn.cursor() 

        sql = f""" 
                SELECT k.JUDUL, ak.NAMA, k.id
                FROM SONG as s, AKUN as ak, KONTEN as k, ARTIST as ar
                WHERE judul ILIKE %s AND s.id_konten = k.id AND ar.email_akun = ak.email AND s.id_artist = ar.id; """

        cursor.execute(sql, (f'%{song}%',)) 
        songs_results= cursor.fetchall()
        
        
        for item in songs_results:
            songs.append({
                'judul':item[0],
                'nama':item[1],
                'id_song':item[2]
            })
        
        print(songs)
        conn.commit() 
        conn.close() 
        
        return JsonResponse({'songs' : songs})

    except psycopg2.Error as e:
        return JsonResponse({'message' : e})

def search_bar_podcasts(request):
    form_data = json.loads(request.body)
    podcast = form_data.get('podcast')
    podcasts = []
    
    try:
        cursor = conn.cursor() 

        sql = f""" 
                SELECT k.JUDUL, ak.NAMA, k.id
                FROM PODCAST as p, AKUN as ak, KONTEN as k
                WHERE judul ILIKE %s AND p.EMAIL_PODCASTER = ak.EMAIL AND p.id_konten = k.id; """

        cursor.execute(sql, (f'%{podcast}%',)) 
        podcasts_results= cursor.fetchall()
        
        print(podcasts_results)
        
        for item in podcasts_results:
            podcasts.append({
                'judul':item[0],
                'nama':item[1],
                'id_konten':item[2]
            })
            
        conn.commit() 
        conn.close() 

        return JsonResponse({'podcasts' : podcasts})

    except psycopg2.Error as e:
        return JsonResponse({'message' : e})
    
def search_bar_user_playlist(request):
    form_data = json.loads(request.body)
    user_playlist = form_data.get('user_playlist')
    user_playlists = []

    try:
        cursor = conn.cursor() 

        sql = f""" SELECT up.JUDUL, ak.NAMA, up.id_playlist
                FROM USER_PLAYLIST as up, AKUN as ak
                WHERE judul ILIKE %s AND up.EMAIL_PEMBUAT = ak.EMAIL;
            """

        cursor.execute(sql, (f'%{user_playlist}%',)) 
        user_playlist_results= cursor.fetchall()
        
        print(user_playlist_results)
        
        for item in user_playlist_results:
            user_playlists.append({
                'judul':item[0],
                'nama':item[1],
                'id_playlist':item[2]
            })
            
        conn.commit() 
        conn.close() 

        return JsonResponse({'user_playlists' : user_playlists})

    except psycopg2.Error as e:
        return JsonResponse({'message' : e})


def song_details(request):
    context = {
    }
    return render(request, "song_details.html", context)
