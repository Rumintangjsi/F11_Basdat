from django.urls import path
from kelola_playlist.views import kelola_playlist, create_playlist

app_name = 'kelola_playlist'

urlpatterns = [
    path('', kelola_playlist, name='kelola_playlist'),
    path('create_playlist/', create_playlist, name='create_playlist'),
]