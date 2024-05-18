from django.urls import path
from play_song.views import play_song, songs, song_played, handle_download, add_song_to_playlist

app_name = 'play_song'

urlpatterns = [
    path('play/<str:song_id>/', play_song, name='play_song'),
    path('songs/', songs, name='songs'),
    path('song_played/', song_played, name='song_played'),
    path('add_song_to_playlist/<str:song_id>', add_song_to_playlist, name='add_song_to_playlist'),
    path('download/song_downloaded/', handle_download, name='song_downloaded'),
]