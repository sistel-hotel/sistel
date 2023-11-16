from django.urls import path
from .views import reservasi_kamar_hotel,detail_hotel, daftar_reservasi_kamar,update_status_reservasi,detail_reservasi
app_name = 'DaftarReservasiHotel'

urlpatterns = [
    path('kamar/', reservasi_kamar_hotel, name= 'reservasi-kamar-hotel'),
    path('detail/', detail_hotel, name= 'detail-hotel'),
    path('daftar-reservasi/', daftar_reservasi_kamar, name= 'daftar-reservasi'),
    path('update-status-reservasi/',update_status_reservasi ),
    path('detail-reservasi/',detail_reservasi )

]
