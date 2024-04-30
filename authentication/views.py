from django.shortcuts import render

def login(request):
    context = {
    
    }

    return render(request, "login.html", context)

def register(request):
    context = {
        
    }

    return render(request, "register.html", context)