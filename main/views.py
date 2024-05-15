from django.db import connection
from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Kelompok',
        'class': 'Basdat F'
    }
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM AKUN")
        row = cursor.fetchall()
        print(row)

    return render(request, "main.html", context)