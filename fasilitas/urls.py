from django.urls import path
from .views import list_hotel_facilities, add_hotel_facility, update_hotel_facility, delete_hotel_facility

urlpatterns = [
    path('hotel_facilities/', list_hotel_facilities, name='list_hotel_facilities'),
    path('hotel_facilities/add/', add_hotel_facility, name='add_hotel_facility'),
    path('hotel_facilities/update/<str:facility_name>/', update_hotel_facility, name='update_hotel_facility'),
    path('delete_facility/<str:facility_name>/<str:hotel_name>/<str:hotel_branch>/', delete_hotel_facility, name='delete_hotel_facility'),
]