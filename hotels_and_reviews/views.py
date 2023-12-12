import json
import math
from django.shortcuts import render, redirect, HttpResponseRedirect
from connect_postgres import execute_sql_query
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import uuid


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



#--------------------------------------------- selesai------------------------------------------------------------------
@csrf_exempt
def daftar_hotel(request):
    user_data = request.session.get('user_data')  # Mendapatkan data sesi 'user_data'
    is_authorized = True
    # Memeriksa apakah data sesi 'user_data' tersedia
    if not user_data:
        # Redirect ke halaman login jika data sesi 'user_data' tidak tersedia
        return redirect('/login/')
    
    query = """
        SELECT DISTINCT hotel.hotel_name, hotel.hotel_branch, hotel.rating, hotel.star,
        COUNT(DISTINCT reviews.id) AS jumlah_review from hotel LEFT JOIN reviews on hotel.hotel_name = reviews.hotel_name 
        and hotel.hotel_branch = reviews.hotel_branch   
        GROUP BY hotel.hotel_name, hotel.hotel_branch, hotel.rating, hotel.star ORDER BY hotel.rating desc, hotel.star desc, jumlah_review desc;
    """
    if user_data['is_hotel'] == True:
        is_authorized = False
        
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
        'is_authorized': is_authorized,
        'username': (user_data['fname'] if user_data['fname'] else '') + ' ' + (user_data['lname'] if user_data['lname'] else ''),
        'is_hotel':user_data['is_hotel']
    }
    return render(request, 'daftar-hotel.html',context)
@csrf_exempt
def detail_hotel(request, nama_hotel, nama_cabang_hotel):
    user_data = request.session.get('user_data')  # Mendapatkan data sesi 'user_data'
    is_authorized = True
    # Memeriksa apakah data sesi 'user_data' tersedia
    if not user_data:
        # Redirect ke halaman login jika data sesi 'user_data' tidak tersedia
        return redirect('/login/')
    
    if(user_data['is_hotel'] == True):
        is_authorized = False
    # -----------------------------------------------------
    if request.method == 'POST':
        id = uuid.uuid4()
        email = request.POST.get("email")
        text = request.POST.get("text")
        rating = request.POST.get("rating")
        query = f"""

        INSERT INTO REVIEWS (id, cust_email, rating, review, hotel_name, hotel_branch) VALUES
        ('{id}', '{email}', {rating}, '{text}', '{nama_hotel}', '{nama_cabang_hotel}')
        RETURNING id;
        """
        execute_sql_query(query=query)
        #TODO: redirect to dashboard 
        return JsonResponse({'url':request.path})
    # ---------------------------------------------------------
    context = {
        'is_hotel_exist':False,
        'email':user_data['email'],
        'hotel': None,
        'reviews': [],
        'available_rooms': {},
        'is_authorized': is_authorized,
        'username': (user_data['fname'] if user_data['fname'] else '') + ' ' + (user_data['lname'] if user_data['lname'] else ''),
        'is_hotel':user_data['is_hotel']
        }
    print(nama_hotel)
    print(nama_cabang_hotel)
    
    print('-------------------------------------------')
    hotel_query = f"""
        SELECT DISTINCT HOTEL.*, REVIEWS.id ,SISTEL.USER.fname, SISTEL.USER.lname, REVIEWS.review, 
        REVIEWS.rating FROM HOTEL
        LEFT JOIN (REVIEWS  INNER JOIN SISTEL.USER ON SISTEL.USER.email = REVIEWS.cust_email) ON HOTEL.hotel_name = REVIEWS.hotel_name AND HOTEL.hotel_branch = REVIEWS.hotel_branch
        WHERE HOTEL.hotel_name = '{nama_hotel}' AND HOTEL.hotel_branch = '{nama_cabang_hotel}';
    """
    matching_hotels = execute_sql_query(hotel_query)
    print('------dibawah ini hotel yang cocok------------------')
    print(matching_hotels)
    if(len(matching_hotels) > 0):
        selected_hotel = matching_hotels[0]
        context['is_hotel_exist'] = True
        context['hotel'] = {
            'hotel_email': selected_hotel[0],
            'hotel_name': selected_hotel[1],
            'hotel_branch': selected_hotel[2],
            'hotel_nib':selected_hotel[3].rstrip('0').rstrip('.') if '.' in selected_hotel[3] else selected_hotel[3],
            'hotel_rating':selected_hotel[4],
            'hotel_star':range(0,int(selected_hotel[5])),
            'hotel_street':selected_hotel[6],
            'hotel_district':selected_hotel[7],
            'hotel_city':selected_hotel[8],
            'hotel_province':selected_hotel[9],
            'hotel_description':selected_hotel[10],
            'hotel_min_checkout':selected_hotel[12].strftime("%H:%M"),
            'hotel_max_checkout': selected_hotel[11].strftime("%H:%M")
        }
        
        for hotel_data in matching_hotels:
            if hotel_data[13] is None:
                continue
            context['reviews'].append({
                'fname':hotel_data[14],
                'lname':hotel_data[15],
                'text':hotel_data[16],
                'rating':hotel_data[17]
            })

        room_query = f"""

            SELECT DISTINCT ROOM.number, ROOM.price, ROOM_FACILITIES.id  FROM ROOM LEFT JOIN ROOM_FACILITIES ON ROOM.number = ROOM_FACILITIES.rnum 
            WHERE ROOM.hotel_name = '{nama_hotel}' AND ROOM.hotel_branch = '{nama_cabang_hotel}' AND 
            ROOM_FACILITIES.hotel_name = '{nama_hotel}' AND ROOM_FACILITIES.hotel_branch = '{nama_cabang_hotel}' AND ROOM.number NOT IN (
                SELECT ROOM.number FROM RESERVATION_ROOM INNER JOIN ROOM ON 
            RESERVATION_ROOM.rnum = ROOM.number WHERE RESERVATION_ROOM.isactive = TRUE AND 
            ROOM.hotel_name = '{nama_hotel}' AND ROOM.hotel_branch = '{nama_cabang_hotel}'
            );
        """
        matching_rooms_data = execute_sql_query(room_query)
        print('---------------- V X ---------------------------')
        print(matching_rooms_data)
        print(len(matching_rooms_data))
        print('---------------- V X ---------------------------')
        for data in matching_rooms_data:
    #//context['available_rooms'] = {}
            room_number = data[0]
            if context['available_rooms'].get(room_number) is None:
                room_data = {
                    'price': data[1],
                    'room_facilities': [data[2]],
                    'room_number':room_number.split('.')[0]
                }
                context['available_rooms'][room_number] = room_data
            else:
                context['available_rooms'][room_number]['room_facilities'].append(data[2])
    
    context['available_rooms'] = list(context['available_rooms'].values())  
    #context['available_rooms'] = []
    print(context['available_rooms'])  
    return render(request, 'detail-hotel-and-reviews.html',context=context)

