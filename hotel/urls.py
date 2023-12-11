from django.urls import path
from .views import dashboard_hotel
app_name = 'hotel'

urlpatterns = [
    path('dashboard/', dashboard_hotel, name= 'dashboard-hotel'),
]
