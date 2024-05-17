from django.shortcuts import render

def show_main(request):
    context = {
        'name': 'Kelompok',
        'class': 'Basdat F'
    }

    return render(request, "main.html", context)