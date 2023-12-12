from django.urls import path
from .views import daftar_hotel,detail_hotel, filter_hotel
app_name = 'hotels_and_reviews'

urlpatterns = [
    path('', daftar_hotel, name= 'daftar-hotel'),
    path('detail/<str:nama_hotel>/<str:nama_cabang_hotel>/', detail_hotel, name= 'detail-hotel'),
    path('filter-hotel/', filter_hotel)
]
