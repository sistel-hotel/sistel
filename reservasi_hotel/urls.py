from django.urls import path
from .views import *
app_name='reservasi_hotel'
urlpatterns = [
    path('hotel/', daftar_reservasi_kamar, name='daftar_reservasi_kamar'),
    path('cust/create-shuttle/<str:rsv_id>', buat_shuttle),
    path('hotel/<str:rsv_id>/update', update_reservation_kamar, name='update_reservation_kamar'),
    path('hotel/<str:rsv_id>/', detail_reservasi),
    
]
