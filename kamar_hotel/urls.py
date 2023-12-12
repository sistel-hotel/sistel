from django.urls import path
from .views import *
app_name = 'kamar_hotel'

urlpatterns = [
    path('', kamar_hotel, name= 'kamar_hotel'),
    path('show_create_kamar_hotel', show_create_kamar_hotel, name='show_create_kamar_hotel')
]