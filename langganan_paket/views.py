from django.shortcuts import render

# Create your views here.
def langganan_paket(request):
    context = {
    }

    return render(request, "langganan_paket.html", context)

def pembayaran_paket(request):
    context = {
    }
    return render(request, "pembayaran_paket.html", context)

def riwayat_transaksi(request):
    context = {
    }
    return render(request, "riwayat_transaksi.html", context)