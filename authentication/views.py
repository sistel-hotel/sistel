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
        # SAMA ---------------------------
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        phone_num = request.POST.get('phone_num')
        # SAMA -------------------------------------
        # HANYA CUSTOMER ---------------------------
        nik = request.POST.get('nik')
        # HANYA HOTEL ------------------------------
        hotel_name = request.POST.get('hotel_name')
        hotel_branch = request.POST.get('hotel_branch')
        nib = request.POST.get('nib')
        star = request.POST.get('star')
        street = request.POST.get('street')
        district = request.POST.get('district')
        city = request.POST.get('city')
        province = request.POST.get('province')
        description = request.POST.get('description')
        min_checkout = request.POST.get('min_checkout')
        max_checkout = request.POST.get('max_checkout')
        print(hotel_name)

        # CEK REGISTER CUSTOMER ATAU HOTEL
        is_customer = True if nik is not None else False

        # CEK CUSTOMER
        if is_customer and not all([email.strip(), password.strip(), confirm_password.strip(), fname.strip(), lname.strip(), nik.strip(), phone_num.strip()]):
            messages.error(request, 'Mohon lengkapi field yang kosong dalam mendaftarkan customer.')
        # CEK HOTEL
        elif not is_customer and not all([email.strip(), password.strip(),
         confirm_password.strip(), fname.strip(), lname.strip(), 
           hotel_name.strip(), hotel_branch.strip(), nib.strip(), star, 
           street.strip(),district.strip(),city.strip(), 
           province.strip(), description.strip(),  
           min_checkout.strip(), max_checkout.strip(), phone_num.strip()]):
            messages.error(request, 'Mohon lengkapi field yang kosong dalam mendaftarkan hotel.')
        # CEK BINTANG
        elif not is_customer and not star.isdigit():
            messages.error(request, 'Maaf, bintang hotel harus bilangan bulat.')
        # CEK RANGE BINTANG
        elif not is_customer and (float(star) < 1 or float(star) > 5):
            messages.error(request, 'Maaf, bintang hotel harus ada di range 1 sampai 5.')
        # CEK PASSWORD
        elif password != confirm_password:
            messages.error(request, 'Password dan konfirmasi password tidak cocok.')
        else:
            if is_customer:
                query= f"""

                INSERT INTO sistel.user  (email, password, fname, lname) VALUES ('{email}','{password}', '{fname}', '{lname}');
                INSERT INTO reservation_actor (email, phonenum) VALUES ('{email}','{phone_num}');
                INSERT INTO customer  (email, nik) VALUES ('{email}','{nik}')
                RETURNING email;
                
                """
            else:
                query = f"""
                INSERT INTO sistel.user  (email, password, fname, lname) VALUES ('{email}','{password}', '{fname}', '{lname}');
                INSERT INTO reservation_actor (email, phonenum) VALUES ('{email}','{phone_num}');
                INSERT INTO hotel 
                (email, hotel_name, hotel_branch, nib, star, street, district, city,
                  province, description, max_checkout, min_checkout) VALUES (
                    '{email}', '{hotel_name}', '{hotel_branch}', '{nib}',
                      {star}, '{street}', '{district}', '{city}', '{province}',
                        '{description}', '{max_checkout}', '{min_checkout}'
                  )
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


    
