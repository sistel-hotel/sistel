from django.urls import path
from .views import *
app_name = 'reservasi'

urlpatterns = [
    path('', show_reservasi_kamar, name= 'show-reservasi'),
    path('complaint/<str:id>', complaint, name= 'complaint'),
    path('complaint/<str:id>/save', save_complaint, name= 'complaint-save'),
    path('dashboard/', dashboard_pengguna, name= 'dashboard-pengguna'),
]
