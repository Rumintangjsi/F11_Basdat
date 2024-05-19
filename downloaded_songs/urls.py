from django.urls import path
from downloaded_songs.views import downloaded_songs, delete_song

app_name = 'downloaded_songs'

urlpatterns = [
    path('', downloaded_songs, name='downloaded_song'),
    path('delete_song/<str:id_song>/', delete_song, name='delete_song')
]