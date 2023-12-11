from django.urls import path
from authentication.views import *

app_name = 'authentication'

urlpatterns = [
    path('', show_home, name='home'),
    path('register/', register_with_postgres, name='register' ),
    path('login/', login_with_postgres, name='login' ),
    path('logout/', logout_with_postgres,name='logout')
]