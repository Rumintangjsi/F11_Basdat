from django.shortcuts import render

def get_royalti(request):
    context = {
    }

    return render(request, "royalti.html", context)