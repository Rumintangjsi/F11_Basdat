from django.urls import path
from royalti.views import get_royalti
app_name = 'royalti'

urlpatterns = [
    path('', get_royalti, name='get_royalti'),
]