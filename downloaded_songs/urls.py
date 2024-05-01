from django.urls import path
from downloaded_songs.views import downloaded_songs

app_name = 'downloadeed_songs'

urlpatterns = [
    path('downloaded_songs/', downloaded_songs, name='downloaded_songs'),
]