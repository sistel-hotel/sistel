import json
from connect_postgres import execute_sql_query
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect
import datetime
import uuid
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.urls import reverse
import psycopg2


def show_home(request):
    return render(request, "home.html")

def show_register(request):
    return render(request, "register.html")

def show_login(request):
    return render(request, "login.html")


def logout_with_postgres(request):
    # Hapus data sesi pengguna
    if 'user_data' in request.session:
        del request.session['user_data']
    
    # Lakukan logout pengguna menggunakan fungsi bawaan Django
    
    # Redirect ke halaman login atau halaman lain yang sesuai
    return redirect('/login/') 

def register_with_postgres(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        nik = request.POST.get('nik')
        phone_num = request.POST.get('phone_num')
        if not all([email.strip(), password.strip(), confirm_password.strip(), fname.strip(), lname.strip(), nik.strip(), phone_num.strip()]):
            messages.error(request, 'Mohon lengkapi field yang kosong.')
        elif password != confirm_password:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
        else:
            query= f"""

            INSERT INTO sistel.user  (email, password, fname, lname) VALUES ('{email}','{password}', '{fname}', '{lname}');
            INSERT INTO reservation_actor (email, phonenum) VALUES ('{email}','{phone_num}');
            INSERT INTO customer  (email, nik) VALUES ('{email}','{nik}')
            RETURNING email;
            
            """
            try:
                execute_sql_query(query=query)
                return HttpResponseRedirect('/login/') 
            except psycopg2.Error as error:
                messages.error(request, f'{error}')
            except Exception as error:
                messages.error(request, f'{error}')
    return render(request,"register.html")

def login_with_postgres(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        query = f"""
    SELECT *,
        CASE WHEN EXISTS (
            SELECT 1 FROM sistel.user u
            INNER JOIN hotel ON u.email = hotel.email
            WHERE u.email = '{email}'
        ) THEN 'false'
        ELSE 'true' END AS is_pengguna
    FROM sistel.user WHERE email = '{email}'
    """
        matching_users = execute_sql_query(query=query)
        
       # print(matching_users)
        if len(matching_users) == 0:
            messages.error(request, 'Pengguna tidak ditemukan.')
        else:
          #  print(matching_users)
            selected_user = matching_users[0]
            user_store_password = selected_user[1]
            user_fname = selected_user[2]
            user_lname = selected_user[3]
            is_user = selected_user[4]
            if user_store_password == password:
                request.session['user_data'] = {
                    'email': email,
                    'fname': user_fname,
                    'lname': user_lname,
                    'is_hotel': is_user == 'false'
                }
                print(request.session['user_data'])
                # TODO: ganti redirect ke dashboard
                return HttpResponseRedirect('/hotels/')  
            messages.error(request, 'Maaf, password yang kamu masukkan salah.')
    return render(request,"login.html")


    
