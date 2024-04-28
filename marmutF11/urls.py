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
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('play_podcast/', include('play_podcast.urls')),
    path('chart/', include('chart.urls')),
    path('chart_detail/', include('chart.urls')),
    path('', include('kelola_podcast.urls')),
    path('podcast_list/', include('kelola_podcast.urls')),
    path('', include('kelola_podcast.urls')),
]
