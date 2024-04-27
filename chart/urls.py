from django.urls import path
from chart.views import chart, chart_detail

app_name = 'chart'

urlpatterns = [
    path('', chart, name='chart'),
    path('chart/chart-detail/', chart_detail, name='chart_detail'),
]