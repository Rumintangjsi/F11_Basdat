"""
URL configuration for marmutF11 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from authentication.views import login, logout, login_api, register, register_pengguna, register_pengguna_api, register_label, register_label_api



urlpatterns = [
    path('register/', register, name='register'),

    path('register/pengguna/', register_pengguna, name='register_pengguna'),
    path('register/pengguna/register_pengguna/', register_pengguna_api, name='register_pengguna_api'),
    
    path('register/label/', register_label, name='register_label'),
    path('register/label/register_label/', register_label_api, name='register_label_api'),

    path('login/', login, name='login'),
    path('login/login_api/', login_api, name='login_api'),

    path('logout/', logout, name='login_api'),

]
