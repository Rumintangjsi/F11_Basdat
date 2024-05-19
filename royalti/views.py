from django.shortcuts import render
from django.db import connection as conn

def get_royalti(request):

    email = request.session['email']
    roles = request.session['role']

    songs = []
    total_royalti = 0

    if ('label' in roles):
        sql = f"""  SELECT 
                        K.judul AS song_title,
                        A.nama AS artist_name,
                        AL.judul AS album_title,
                        S.total_play AS plays,
                        S.total_download AS downloads,
                        L.nama AS label_name,
                        L.email AS label_email,
                        PHC.rate_royalti AS label_royalty_rate,
                        (S.total_play * PHC.rate_royalti) AS total_label_royalty_amount
                    FROM 
                        SONG S
                        JOIN KONTEN K ON S.id_konten = K.id
                        JOIN ARTIST AR ON S.id_artist = AR.id
                        JOIN AKUN A ON AR.email_akun = A.email
                        JOIN ALBUM AL ON S.id_album = AL.id
                        JOIN LABEL L ON AL.id_label = L.id
                        JOIN PEMILIK_HAK_CIPTA PHC ON L.id_pemilik_hak_cipta = PHC.id
                    WHERE 
                        L.email = %s
                """
        
        cursor = conn.cursor() 

        cursor.execute(sql, (email, ))
        results = cursor.fetchall()
       
        for item in results:
            songs.append({
                'title' : item[0],
                'album' : item[2],
                'artist' : item[1],
                'plays' : item[3],
                'downloads' : item[4],
                'royalti' : item[8]
            })

            total_royalti += item[8]
        
        context = {
            'total_royalti' : total_royalti,
            'songs' : songs
        }

        return render(request, "royalti.html", context)

    if 'artist' in roles: 
        sql = f"""  SELECT 
                        K.judul AS song_title,
                        A.nama AS artist_name,
                        AL.judul AS album_title,
                        S.total_play AS plays,
                        S.total_download AS downloads,
                        PHC.rate_royalti AS royalty_rate,
                        (S.total_play * PHC.rate_royalti) AS total_royalty_amount
                    FROM 
                        SONG S
                        JOIN KONTEN K ON S.id_konten = K.id
                        JOIN ARTIST AR ON S.id_artist = AR.id
                        JOIN AKUN A ON AR.email_akun = A.email
                        JOIN ALBUM AL ON S.id_album = AL.id
                        JOIN ROYALTI R ON S.id_konten = R.id_song
                        JOIN PEMILIK_HAK_CIPTA PHC ON R.id_pemilik_hak_cipta = PHC.id
                    WHERE 
                        A.email = %s
                """
                
        cursor = conn.cursor() 

        cursor.execute(sql, (email, ))
        results = cursor.fetchall()
       
        for item in results:
            songs.append({
                'title' : item[0],
                'album' : item[2],
                'artist' : item[1],
                'plays' : item[3],
                'downloads' : item[4],
                'royalti' : item[6]
            })
            total_royalti += item[6]

    if 'songwriter' in roles:
        sql = f"""  SELECT 
                        K.judul AS song_title,
                        A.nama AS songwriter_name,
                        AL.judul AS album_title,
                        S.total_play AS plays,
                        S.total_download AS downloads,
                        PHC.rate_royalti AS royalty_rate,
                        (S.total_play * PHC.rate_royalti) AS total_royalty_amount
                    FROM 
                        SONG S
                        JOIN KONTEN K ON S.id_konten = K.id
                        JOIN SONGWRITER_WRITE_SONG SWS ON S.id_konten = SWS.id_song
                        JOIN SONGWRITER SW ON SWS.id_songwriter = SW.id
                        JOIN AKUN A ON SW.email_akun = A.email
                        JOIN ALBUM AL ON S.id_album = AL.id
                        JOIN PEMILIK_HAK_CIPTA PHC ON SW.id_pemilik_hak_cipta = PHC.id
                    WHERE 
                        A.email = %s
                """
                
        cursor = conn.cursor() 

        cursor.execute(sql, (email, ))
        results = cursor.fetchall()

        print(results)
       
        for item in results:
            songs.append({
                'title' : item[0],
                'album' : item[2],
                'artist' : item[1],
                'plays' : item[3],
                'downloads' : item[4],
                'royalti' : item[6]
            })
            total_royalti += item[6]        

    context = {
        'total_royalti' : total_royalti,
        'songs' : songs
    }

    return render(request, "royalti.html", context)