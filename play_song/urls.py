from django.urls import path
from play_song.views import play_song, add_song_playlist, downloaded_song, songs

app_name = 'play_song'

urlpatterns = [
    path('<str:song_id>/', play_song, name='play_song'),
    path('songs/', songs, name='songs'),
    path('add-song-playlist/', add_song_playlist, name='add_song_playlist'),
    path('download/list/', downloaded_song, name='download_song'),
]