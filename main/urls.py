from django.urls import path
from main.views import show_main, dashboard

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('dashboard/', dashboard, name='show_main'),
]