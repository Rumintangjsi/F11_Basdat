from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render
import psycopg2
import uuid

conn = psycopg2.connect( 
    database="railway", 
    user='postgres', 
    password='pCIIFIIJGgOGhPBgjASGQVjzXEOYPumt', 
    host='viaduct.proxy.rlwy.net', 
    port='59310'
)

conn.autocommit = True

def langganan_paket(request):
        
    paket = []

    try:
        cursor = conn.cursor() 

        sql = """ SELECT * from paket """

        cursor.execute(sql) 
        results = cursor.fetchall()
        
        for item in results:
            paket.append({
                'jenis':item[0],
                'harga':item[1]
            })
            
            
        conn.commit() 
        conn.close() 

    except psycopg2.Error as e:
        print("Error connecting to database:", e)


    context = {
        'paket' : paket
    }

    return render(request, "langganan_paket.html", context)

def pembayaran_paket(request, jenis, harga):
    context = {
        'jenis':jenis,
        'harga':harga
    }
    return render(request, "pembayaran_paket.html", context)

def bayar_paket(request):
    data = request.GET.get('data')
    data_list = data.split(',')
    
    id = uuid.uuid4()
    if len(data_list) == 3:
        jenis_paket = data_list[0]
        nominal = data_list[1]
        metode_bayar = data_list[2]
    
    list_paket = jenis_paket.split(' ')
    bulan = int(list_paket[0])
    
    email = "qsmith@example.org"
    timestamp_dimulai = timezone.now()
    timestamp_berakhir = timestamp_dimulai+ timedelta(days=bulan*30)
    
    try:
        cursor = conn.cursor() 
            
        sql = """ 
                INSERT INTO transaction (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        cursor.execute(sql, (
            id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal
        ))
        conn.commit() 
        conn.close() 
    except psycopg2.Error as e:
        print("Error connecting to database:", e)
  
    return JsonResponse({})

def riwayat_transaksi(request):
    riwayat = []

    try:
        cursor = conn.cursor() 

        sql = """ SELECT * from transaction """

        cursor.execute(sql) 
        results = cursor.fetchall()
        
        for item in results:
            riwayat.append({
                'jenis_paket':item[1],
                'timestamp_dimulai':item[3],
                'timestamp_berakhir':item[4],
                'metode_bayar':item[5],
                'nominal':item[6]
            })
            
            
        conn.commit() 
        conn.close() 

    except psycopg2.Error as e:
        print("Error connecting to database:", e)


    context = {
        'riwayat' : riwayat
    }


    return render(request, "riwayat_transaksi.html", context)

