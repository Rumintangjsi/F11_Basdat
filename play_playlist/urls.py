from django.urls import path
from play_playlist.views import add_song_playlist, play_playlist, delete_song_playlist

app_name = 'play_playlist'

urlpatterns = [
    path('<str:playlist_id>/', play_playlist, name='play_playlist'),
    path('add-song-playlist/<str:playlist_id>', add_song_playlist, name='add_song_playlist'),
    path('delete-song-playlist/<str:playlist_id>/<str:song_id>', delete_song_playlist, name='delete_song_playlist'),
]