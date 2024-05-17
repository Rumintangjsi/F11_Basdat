from django.urls import path
from search_bar.views import search_bar_songs, song_details, search_bar_podcasts, search_bar_user_playlist, search

app_name = 'search_bar'

urlpatterns = [
    path('search_bar_songs/', search, name='search_bar_songs'),
    path('search_bar_songs/search_bar_songs/', search_bar_songs, name='search_bar_songs'),
    path('search_bar_songs/search_bar_podcast/', search_bar_podcasts, name='search_bar_podcast'),
    path('search_bar_songs/search_bar_user_playlist/', search_bar_user_playlist, name='search_bar_user_playlist'),
    path('song_details/', song_details, name='song_details'),
    
]