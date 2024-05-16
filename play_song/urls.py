from django.urls import path
from play_song.views import play_song, songs

app_name = 'play_song'

urlpatterns = [
    path('<str:song_id>/', play_song, name='play_song'),
    path('songs/', songs, name='songs'),
]