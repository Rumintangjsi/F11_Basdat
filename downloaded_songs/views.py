from django.shortcuts import render
import psycopg2

conn = psycopg2.connect( 
    database="railway", 
    user='postgres', 
    password='pCIIFIIJGgOGhPBgjASGQVjzXEOYPumt', 
    host='viaduct.proxy.rlwy.net', 
    port='59310'
)
# Create your views here.
def downloaded_songs(request, email):
    email = request.session['email']
    premium_acc = []
    
    try:
        cursor = conn.cursor()
    
        sql = f"""
                SELECT * FROM premium
                """
        cursor.execute(sql) 
        results = cursor.fetchall()
        
        for item in results:
            premium_acc.append({
                'email':item[0]
            })
        conn.commit()
        
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
    
    
    
    context = {
    }
    return render(request, "downloaded_songs.html", context)