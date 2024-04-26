from django.shortcuts import render

def chart(request):
    context = {
        'name': 'Kelompok',
        'class': 'Basdat F'
    }

    return render(request, "chart.html", context)