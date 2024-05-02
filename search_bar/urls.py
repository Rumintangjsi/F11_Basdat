from django.urls import path
from search_bar.views import search_bar

app_name = 'search_bar'

urlpatterns = [
    path('search_bar/', search_bar, name='search_bar'),
   
]