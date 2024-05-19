import json
import uuid
import re

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection as conn
from psycopg2.extras import DateRange

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def register_pengguna(request):
    return render(request, "register_pengguna.html")

def register_label(request):
    return render(request, "register_label.html")

def register_pengguna_api(request):

    if request.method == 'POST':
        form_data = json.loads(request.body)
        email = form_data.get('email')
        password = form_data.get('password')
        nama = form_data.get('nama')
        tempat_lahir = form_data.get('tempat_lahir')
        tanggal_lahir = form_data.get('tanggal_lahir')
        kota_asal = form_data.get('kota_asal')

        artist = form_data.get('artist')
        songwriter = form_data.get('songwriter')
        podcaster = form_data.get('podcaster')

        gender = 0 if form_data.get('gender') == 'Perempuan' else 1
        is_verified = True if (artist is not None or 
                               songwriter is not None or 
                               podcaster is not None) else False
        
        if not check(email) :
            return JsonResponse({'error': 'Email is not valid'}, status=400)
        
        sql = f"""
            INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor = conn.cursor() 
        cursor.execute(sql, (email, password, nama, gender, tempat_lahir, tanggal_lahir, is_verified, kota_asal))
        conn.commit()

        if (is_verified):
            hak_cipta_id = uuid.uuid4()
            rate_royalti = 50

            sql = f"""
                INSERT INTO pemilik_hak_cipta (id, rate_royalti) 
                VALUES (%s, %s)
            """
            
            cursor.execute(sql, (hak_cipta_id, rate_royalti))
            conn.commit()

        if artist is not None:
            artist_id = uuid.uuid4()

            sql = f"""
                INSERT INTO artist (id, email_akun, id_pemilik_hak_cipta) 
                VALUES (%s, %s, %s)
            """
            
            cursor.execute(sql, (artist_id, email, hak_cipta_id))
            conn.commit()
            
        
        if songwriter is not None:
            songwriter_id = uuid.uuid4()

            sql = f"""
                INSERT INTO songwriter (id, email_akun, id_pemilik_hak_cipta) 
                VALUES (%s, %s, %s)
            """
            
            cursor.execute(sql, (songwriter_id, email, hak_cipta_id))
            conn.commit()

        if podcaster is not None:

            sql = f"""
                INSERT INTO podcaster (email) 
                VALUES (%s)
            """
            
            cursor.execute(sql, (email,))
            conn.commit()

        
        return JsonResponse({'message': 'Pengguna created successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
def register_label_api(request):

    # TODO Regis Validation Logic

    if request.method == 'POST':
        form_data = json.loads(request.body)
        email = form_data.get('email')
        password = form_data.get('password')
        nama = form_data.get('nama')
        kontak = form_data.get('kontak')

        hak_cipta_id = uuid.uuid4()
        rate_royalti = 50

        if not check(email) :
            return JsonResponse({'error': 'Email is not valid'}, status=400)

        sql = f"""
            INSERT INTO pemilik_hak_cipta (id, rate_royalti) 
            VALUES (%s, %s)
        """
        
        cursor = conn.cursor() 
        cursor.execute(sql, (hak_cipta_id, rate_royalti))
        conn.commit()

        label_id = uuid.uuid4()

        sql = f"""
            INSERT INTO label (id, nama, email, password, kontak, id_pemilik_hak_cipta) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (label_id, nama, email, password, kontak, hak_cipta_id))
        conn.commit()
            
        return JsonResponse({'message': 'Label created successfully'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def login_api(request):
    if request.method == 'POST':
        form_data = json.loads(request.body)
        email = form_data.get('email')
        password = form_data.get('password')

        if not check(email) :
            return JsonResponse({'error': 'Email is not valid'}, status=400)
        
        # Label login
        sql = f"""
            SELECT email, password FROM label WHERE email = %s """
        
        cursor = conn.cursor() 
        cursor.execute(sql, (email, ))
        results = cursor.fetchone()

        if results :
            db_pass = results[1]

            if password != db_pass:
                return JsonResponse({'error': 'Wrong password'}, status=405)
            else:
                request.session['email'] = email
                request.session['role'] = ["label"]
                return JsonResponse({'message': 'Label login Success'})
        
        # Pengguna login
        sql = f"""
            SELECT email, password FROM akun WHERE email = %s """
        
        cursor = conn.cursor() 
        cursor.execute(sql, (email, ))
        results = cursor.fetchone()

        if results :
            db_pass = results[1]

            if (not results) :
                return JsonResponse({'error': 'Email not found'}, status=405)
        
            if (password != db_pass) :
                return JsonResponse({'error': 'Wrong password'}, status=405)

            conn.commit()

            role = []

            # Check if email exists in the artist table
            sql = "SELECT email_akun FROM artist WHERE email_akun = %s"
            cursor.execute(sql, (email,))
            artist = cursor.fetchone()
            print(artist)
            if artist:
                role.append("artist")

            # Check if email exists in the songwriter table
            sql = "SELECT email_akun FROM songwriter WHERE email_akun = %s"
            cursor.execute(sql, (email,))
            songwriter = cursor.fetchone()
            print(songwriter)
            if songwriter:
                role.append("songwriter")

            # Check if email exists in the podcaster table
            sql = "SELECT email FROM podcaster WHERE email = %s"
            cursor.execute(sql, (email,))
            podcaster = cursor.fetchone()
            print(podcaster)
            if podcaster:
                role.append("podcaster")

            request.session['email'] = email
            request.session['role'] = role

            return JsonResponse({'message': 'Login Success'})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

def check(email):
    
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    if (re.fullmatch(regex, email)):
        return True
    else:
        return False