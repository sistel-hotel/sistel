from django.shortcuts import render

# Create your views here.

def reservasi_kamar_hotel(request):
    return render(request, 'reservasi-kamar-hotel.html')
def detail_hotel(request):
    return render(request, 'detail-hotel.html')
def daftar_reservasi_kamar(request):
    return render(request, 'daftar-reservasi-kamar.html')
def update_status_reservasi(request):
    return render(request, "update-status-page.html")
def detail_reservasi(request):
    return render(request, "detail-reservasi.html")