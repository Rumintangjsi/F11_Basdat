from django.urls import path
from play_playlist.views import play_playlist

app_name = 'play_playlist'

urlpatterns = [
    path('', play_playlist, name='play_playlist'),
]