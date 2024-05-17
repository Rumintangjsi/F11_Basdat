from django.urls import path
from kelola_playlist.views import create_playlist_post, kelola_playlist, create_playlist_page, delete_playlist, edit_playlist_post, edit_playlist_page

app_name = 'kelola_playlist'

urlpatterns = [
    path('', kelola_playlist, name='kelola_playlist'),
    path('create_playlist/', create_playlist_page, name='create_playlist'),
    path('create_playlist_post/', create_playlist_post, name='create_playlist_post'),
    path('delete_playlist/<str:id_playlist>', delete_playlist, name='delete_playlist'),
    path('edit_playlist/<str:id_playlist>', edit_playlist_page, name='edit_playlist'),
    path('edit_playlist_post/<str:id_playlist>', edit_playlist_post, name='edit_playlist_post'),
]