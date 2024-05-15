from django.urls import path
from play_song.views import play_song, add_song_playlist, download_song, songs

app_name = 'play_song'

urlpatterns = [
    path('', play_song, name='play_song'),
    path('songs/', songs, name='songs'),
    path('add_song_playlist/', add_song_playlist, name='add_song_playlist'),
    path('download_song/', download_song, name='download_song'),
]