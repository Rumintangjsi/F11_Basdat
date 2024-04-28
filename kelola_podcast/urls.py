from django.urls import path
from kelola_podcast.views import kelola_podcast

app_name = 'kelola_podcast'

urlpatterns = [
    path('', kelola_podcast, name='kelola_podcast'),
]