from django.urls import path
from langganan_paket.views import langganan_paket, pembayaran_paket, riwayat_transaksi

app_name = 'langganan_paket'

urlpatterns = [
    path('pembayaran_paket/', pembayaran_paket, name='pembayaran_paket'),
    path('langganan_paket/', langganan_paket, name='langganan_paket'),
    path('riwayat_transaksi/', riwayat_transaksi, name='riwayat_transaksi'),
]