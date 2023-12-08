import json
import math
from django.shortcuts import render, redirect
from connect_postgres import execute_sql_query
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def filter_hotel(request):
    data = json.loads(request.body)
    print(data)
    print('------------------------------------------------')
    max_price = data['max_price']
    min_price = data['min_price']

    query = f"""
        SELECT DISTINCT h.hotel_name, h.hotel_branch, h.rating, h.star, COUNT(DISTINCT rev.id) ,MIN(r.price)
        FROM hotel h
        INNER JOIN room r ON h.hotel_name = r.hotel_name AND h.hotel_branch = r.hotel_branch
        LEFT JOIN reviews rev ON h.hotel_name = rev.hotel_name AND h.hotel_branch = rev.hotel_branch
        WHERE r.price >= {min_price} AND r.price <= {max_price} GROUP BY h.hotel_name, h.hotel_branch, h.rating, h.star;
    """
    lst = []
    res = execute_sql_query(query)
    for row in res:
        data = {
            'hotel_name': row[0],
            'hotel_branch':row[1],
            'hotel_rating':row[2],
            'hotel_star': int(row[3]),
            'reviews_count':row[4] if row[4] is not None else 0,
            'min_price':row[5]
        }
        lst.append(data)
    print(res)
    return JsonResponse({'hotels':lst})

def reservasi_kamar_hotel(request):
    user_data = request.session.get('user_data')  # Mendapatkan data sesi 'user_data'

    # Memeriksa apakah data sesi 'user_data' tersedia
    if not user_data:
        # Redirect ke halaman login jika data sesi 'user_data' tidak tersedia
        return redirect('/login/')
    
    query = """
        SELECT DISTINCT hotel.hotel_name, hotel.hotel_branch, hotel.rating, hotel.star,
        COUNT(DISTINCT reviews.id) from hotel LEFT JOIN reviews on hotel.hotel_name = reviews.hotel_name 
        and hotel.hotel_branch = reviews.hotel_branch   
        GROUP BY hotel.hotel_name, hotel.hotel_branch, hotel.rating, hotel.star limit 5;
    """
    lst = []
    res = execute_sql_query(query=query)
    print(res)
    for row in res:
        data = {
            'hotel_name': row[0],
            'hotel_branch':row[1],
            'hotel_rating':row[2],
            'hotel_star': int(row[3]),
            'filled_stars':range(0,int(row[3])),
            'reviews_count':row[4] if row[4] is not None else 0
        }
        lst.append(data)
    context = {
        'hotels':lst,
        'username': (user_data['fname'] if user_data['fname'] else '') + ' ' + (user_data['lname'] if user_data['lname'] else ''),
        'is_hotel':user_data['is_hotel']
    }
    return render(request, 'reservasi-hotel.html',context)
def detail_hotel(request):

    return render(request, 'detail-hotel.html')
def daftar_reservasi_kamar(request):
   
    return render(request, 'daftar-reservasi-kamar.html')
def update_status_reservasi(request):
    return render(request, "update-status-page.html")
def detail_reservasi(request):
    return render(request, "detail-reservasi.html")