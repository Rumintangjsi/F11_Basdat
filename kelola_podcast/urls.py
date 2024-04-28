from django.urls import path
from kelola_podcast.views import create_podcast, podcast_list, create_episode

app_name = 'kelola_podcast'

urlpatterns = [
    path('create_podcast/', create_podcast, name='create_podcast'),
    path('podcast_list/', podcast_list, name='podcast_list'),
    path('podcast_list/create_episode/', create_episode, name='create_episode'),
]