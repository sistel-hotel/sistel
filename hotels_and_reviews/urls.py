from django.urls import path
from .views import daftar_hotel,detail_hotel, daftar_reservasi_kamar,update_status_reservasi,detail_reservasi, filter_hotel
app_name = 'hotels_and_reviews'

urlpatterns = [
    path('', daftar_hotel, name= 'daftar-hotel'),
    path('detail/<str:nama_hotel>/<str:nama_cabang_hotel>/', detail_hotel, name= 'detail-hotel'),
    path('reservation-list/', daftar_reservasi_kamar, name= 'daftar-reservasi'),
    path('update-status-reservasi/',update_status_reservasi ),
    path('detail-reservasi/',detail_reservasi ),
    path('filter-hotel/', filter_hotel)

]
