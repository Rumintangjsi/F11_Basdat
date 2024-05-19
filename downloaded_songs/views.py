from django.http import HttpResponse
from django.shortcuts import redirect, render
import psycopg2

conn = psycopg2.connect( 
    database="railway", 
    user='postgres', 
    password='pCIIFIIJGgOGhPBgjASGQVjzXEOYPumt', 
    host='viaduct.proxy.rlwy.net', 
    port='59310'
)
# Create your views here.
def downloaded_songs(request):
    email = request.session['email']
    premium_acc = []
    akun = []
    
    try:
        cursor = conn.cursor()
    
        sql = f"""
                SELECT * FROM AKUN
                """
        cursor.execute(sql) 
        results = cursor.fetchall()

        for item in results:
            akun.append(item[0])
        conn.commit()
        print("ini akun")
        print(akun)
            
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
    
    try:
        cursor = conn.cursor()
    
        sql = f"""
                SELECT * FROM premium
                """
        cursor.execute(sql) 
        results = cursor.fetchall()

        for item in results:
            premium_acc.append(item[0])
        conn.commit()
        print("ini premium")
        print(premium_acc)
        
        
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
        
    if email not in akun:
        print("not found")
        context = {
            'message':'not found'
        }
        return render(request, "downloaded_songs.html", context)
    elif email in premium_acc:
        print("anjir")
        return downloaded_song_view(request, email)
    elif email not in premium_acc:
        print("bukan premium")
        context = {
            'message':'Anda bukan premium'
        }
        return render(request, "downloaded_songs.html", context)
    
    
def downloaded_song_view(request, email):
    email = request.session['email']
    list_downloaded = []

    try:
        cursor = conn.cursor()
    
        sql = f"""
                SELECT k.judul, ak.nama, k.id
                FROM downloaded_song ds
                INNER JOIN song s ON ds.id_song = s.id_konten
                INNER JOIN konten k ON s.id_konten = k.id
                INNER JOIN artist ar ON s.id_artist = ar.id
                INNER JOIN akun ak ON ar.email_akun = ak.email
                WHERE ds.email_downloader = %s;
                """
        cursor.execute(sql, (email,)) 
        results = cursor.fetchall()
        
        
        for item in results:
            list_downloaded.append({
                'judul':item[0],
                'nama':item[1],
                'id':item[2] 
            })
        conn.commit()

        
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
      
    context={
        'list_download':list_downloaded
    }
    context2={
        'message':'Anda tidak memiliki lagu yang diunduh'
    }
    if len(list_downloaded) ==0:
        return render(request, "downloaded_songs.html", context2)
    elif list_downloaded != 0:
        return render(request, "downloaded_songs.html", context)
    
    

def delete_song(request, id_song):
    if request.method == 'DELETE':
        cursor = conn.cursor() 
        sql = f""" DELETE FROM downloaded_song WHERE id_song = %s """
        cursor.execute(sql, (id_song,))
        conn.commit()
        print("ke klik")
        
        return render(request, "downloaded_songs.html")