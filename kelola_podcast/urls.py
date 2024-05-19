from django.urls import path
from kelola_podcast.views import create_podcast, podcast_list, create_episode, episode_list, delete_episode, delete_podcast

app_name = 'kelola_podcast'

urlpatterns = [
    path('create_podcast/<str:email_podcaster>/', create_podcast, name='create_podcast'),
    path('podcast_list/<str:email_podcaster>/', podcast_list, name='podcast_list'),
    path('podcast_list/<uuid:id_konten>/create_episode/', create_episode, name='create_episode'),
    path('podcast_list/episode_list/<uuid:podcast_id>/', episode_list, name='episode_list'),
    path('podcast_list/delete_episode/<uuid:episode_id>/', delete_episode, name='delete_episode'),
    path('podcast_list/delete_podcast/<uuid:podcast_id>/', delete_podcast, name='delete_podcast'),
]