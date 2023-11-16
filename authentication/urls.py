from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', show_home, name='home'),
    path('register/', show_register, name='register' ),
    path('login/', show_login, name='login' ),
]