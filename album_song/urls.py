from django.urls import path
from album_song.views import album_list, song_list, fetch_album, fetch_song, add_song, edit_song, delete_song, add_album, edit_album, delete_album
app_name = 'album_song'

urlpatterns = [
    path('', album_list, name='album_list'),
    path('<uuid:album_id>/', song_list, name='song_list'),
    
    path('fetch_album/', fetch_album, name='fetch_album'),
    path('fetch_song/', fetch_song, name='fetch_song'),

    path('add_album/', add_album, name='add_album'),
    path('edit_album/<str:album_id>', edit_album, name='edit_album'),
    path('delete_album/<str:album_id>', delete_album, name='delete_album'),

    path('add_song/', add_song, name='add_song'),
    path('edit_song/<str:song_id>', edit_song, name='edit_song'),
    path('delete_song/<str:konten_id>', delete_song, name='delete_song'),

]