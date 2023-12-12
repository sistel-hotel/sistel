from django.urls import path
from .views import *
app_name = 'reservasi'

urlpatterns = [
    path('', show_reservasi_kamar, name= 'show-reservasi'),
    path('complaint/<str:id>', complaint, name= 'complaint'),
    path('complaint/<str:id>/save', save_complaint, name= 'complaint-save'),
    path('buat', buat_reservasi, name= 'buat-reservasi'),
    path('detail/<str:id>', detail_reservasi, name= 'detail-reservasi'),
    path('complaint/<str:id>', complaint, name= 'complaint'),
    path('complaint/<str:id>/save', save_complaint, name= 'complaint-save'),
    path('cancel/<str:id>', cancel_reservasi, name= 'cancel-reservasi'),
    path('dashboard/', dashboard_pengguna, name= 'dashboard-pengguna'),
]
