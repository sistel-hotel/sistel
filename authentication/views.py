import re
from django.shortcuts import render
import datetime
import uuid
from django.shortcuts import render, redirect
from django.db import connection, InternalError
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def show_home(request):
    return render(request, "home.html")

def show_register(request):
    return render(request, "register.html")

def show_login(request):
    return render(request, "login.html")