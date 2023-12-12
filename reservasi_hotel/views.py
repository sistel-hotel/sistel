from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from connect_postgres import execute_sql_query
from django.contrib import messages
from datetime import datetime

@csrf_exempt
def buat_shuttle(request, rsv_id):
    session_data = request.session.get('user_data')
    print(session_data)
    if not session_data:
        return redirect('/login/')
    if request.method == 'POST':
        ordered_vehicle_platnum = request.POST.get('platnum')

        try:
            ordered_driver_query = f"""
            SELECT DRIVER.phonenum FROM DRIVER ORDER BY random() LIMIT 1;
            """
            ordered_driver = execute_sql_query(ordered_driver_query)[0]
            current_date = datetime.now().strftime("%Y-%m-%d")
            order_shuttleservice_query = f"""
                INSERT INTO RESERVATION_SHUTTLESERVICE (rsv_id, vehicle_num, driver_phonenum, datetime, isactive) VALUES
                ('{rsv_id}', '{ordered_vehicle_platnum}', '{ordered_driver[0]}', '{current_date}', TRUE )
                RETURNING rsv_id;
                
            """
            execute_sql_query(order_shuttleservice_query)
            select_shuttle = f""" SELECT * FROM SHUTTLE_SERVICES WHERE driver_phonenum = '{ordered_driver[0]}' AND
            vehicle_platnum = '{ordered_vehicle_platnum}';
            """
            res = execute_sql_query(select_shuttle)
            if len(res) == 0:
                execute_sql_query(f"""
            INSERT INTO SHUTTLE_SERVICES (driver_phonenum, vehicle_platnum)
                VALUES ('{ordered_driver[0]}', '{ordered_vehicle_platnum}')
                RETURNING driver_phonenum;
            """)
        except Exception as err:
            print(err)
            messages.error(request=request, message=err)
    get_vehicles_query = f"""
    SELECT DISTINCT VEHICLE.platnum, VEHICLE.vehicle_brand, VEHICLE.vehicle_type FROM VEHICLE;
    """
    vehicle_data = execute_sql_query(get_vehicles_query)
    vehicles = [

    ]
    for vehicle in vehicle_data:
        vehicles.append({
            'platnum': vehicle[0],
            'vehicle_name': vehicle[1] + " " + vehicle[2]
        })

    return render(request=request, template_name='buat-shuttle.html',
                   context={'reservation_id':rsv_id,'vehicles': vehicles})




    

@csrf_exempt
def update_reservation_kamar(request, rsv_id):
    session_data = request.session.get('user_data')
    is_authorized = True
    print(session_data)
    if not session_data:
        return redirect('/login/')
    if session_data['is_hotel'] == False:
        is_authorized = False
    if request.method == 'POST':
        selected_status_id = request.POST.get('status')
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if selected_status_id is not None:
            query  = f"""
            UPDATE RESERVATION_STATUS_HISTORY 
            SET rsid = '{selected_status_id}', datetime = '{current_datetime}'
            WHERE rid = '{rsv_id}' RETURNING rid;
        """
            try:
                update_status_res = execute_sql_query(query=query)
                print(update_status_res)
                return redirect('/reservasi-hotel/hotel')
            except Exception as err:
                messages.error(request=request,message=err)
        
    query = f"""
    SELECT DISTINCT RESERVATION_ROOM.rnum, RESERVATION_STATUS.status, RESERVATION_STATUS.id, RESERVATION_STATUS_HISTORY.datetime FROM RESERVATION_ROOM  
    LEFT JOIN (RESERVATION_STATUS_HISTORY INNER JOIN RESERVATION_STATUS ON
    RESERVATION_STATUS_HISTORY.rsid = RESERVATION_STATUS.id) ON RESERVATION_ROOM.rsv_id =
    RESERVATION_STATUS_HISTORY.rid WHERE RESERVATION_ROOM.rsv_id = '{rsv_id}' ORDER BY 
    RESERVATION_STATUS_HISTORY.datetime DESC LIMIT 1
"""
    res = execute_sql_query(query=query)
    if len(res) == 0:
        return HttpResponseNotFound('Maaf update reservasi tidak bisa dilakukan')
    status_query = f"""
    SELECT DISTINCT RESERVATION_STATUS.id, RESERVATION_STATUS.status FROM RESERVATION_STATUS
"""
    res = res[0]
    status_res = execute_sql_query(status_query)
    status_lst = []
    for status_data in status_res:
        status_lst.append({
            'status_id': status_data[0],
            'status_title':status_data[1],
            'is_selected': res[2] == status_data[0]
        })

    context = {
        'is_hotel':is_authorized,
        'reservation_id':rsv_id,
        'reservation_room_number':res[0].split('.')[0],
        'reservation_status':res[1],
        'reservation_status_id':res[2],
        'status':status_lst
    }
    print(res)
    return render(request=request, template_name='update-reservasi-by-hotel.html', context=context)


#asumsi:shuttle max 1 tiap reservasi
@csrf_exempt
def detail_reservasi(request, rsv_id):
    session_data = request.session.get('user_data')
    is_authorized = True
    #print(session_data)
    if not session_data:
        return redirect('/login/')
    if session_data['is_hotel'] == False:
        is_authorized = False
    query = f"""
    SELECT DISTINCT RESERVATION_ROOM.rnum, RESERVATION_ROOM.rhotelname, 
    RESERVATION_ROOM.rhotelbranch, RESERVATION_ROOM.datetime, 
    RESERVATION_STATUS.status, RESERVATION_SHUTTLESERVICE.rsv_id, RESERVATION_STATUS_HISTORY.datetime,
    RESERVATION_SHUTTLESERVICE.vehicle_num, RESERVATION_SHUTTLESERVICE.driver_phonenum, 
    RESERVATION_SHUTTLESERVICE.datetime
    
    FROM (RESERVATION_ROOM LEFT JOIN (RESERVATION_STATUS_HISTORY INNER JOIN RESERVATION_STATUS ON
    RESERVATION_STATUS_HISTORY.rsid = RESERVATION_STATUS.id) 
    ON RESERVATION_ROOM.rsv_id = RESERVATION_STATUS_HISTORY.rid) 
    LEFT JOIN RESERVATION_SHUTTLESERVICE 
    ON RESERVATION_ROOM.rsv_id = RESERVATION_SHUTTLESERVICE.rsv_id WHERE
    RESERVATION_ROOM.rsv_id = '{rsv_id}'  ORDER BY 
    RESERVATION_STATUS_HISTORY.datetime DESC, RESERVATION_SHUTTLESERVICE.datetime DESC
    LIMIT 1
"""
    #AND RESERVATION_ROOM.isactive = TRUE
    res = execute_sql_query(query=query)
    if len(res) == 0:
        return HttpResponseNotFound('Maaf detail reservasi tidak ditemukan')
    res = res[0]
    context = {
        'is_hotel':is_authorized,
        'reservation_id': rsv_id,
        'reservation_room_number': res[0],
        'reservation_hotel_name': res[1],
        'reservation_hotel_branch': res[2],
        'reservation_room_time':res[3],
        'reservation_status':res[4],
        'is_shuttle_exist': res[5] is not None,
        'shuttle_vehicle_num':res[7] if res[7] is not None else '-',
        'shuttle_driver_num':res[8] if res[8] is not None else '-',
        'shuttle_time':res[9] if res[9] is not None else '-'
    }
    print(context)
    print(res)
    return render(request=request,template_name="detail-reservasi.html", context=context)

#END
@csrf_exempt
def  daftar_reservasi_kamar(request):
    session_data = request.session.get('user_data')

    is_authorized = True
    print(session_data)
    if not session_data:
        return redirect('/login/')
    if session_data['is_hotel'] == False:
        is_authorized = False
    query = f"""
    SELECT DISTINCT RESERVATION_ROOM.rsv_id, RESERVATION_ROOM.rnum, RESERVATION_STATUS.status ,
    RESERVATION_ROOM.datetime,RESERVATION_STATUS_HISTORY.datetime FROM 
    (RESERVATION_ROOM INNER JOIN RESERVATION_STATUS_HISTORY ON RESERVATION_STATUS_HISTORY.rid = 
    RESERVATION_ROOM.rsv_id INNER JOIN RESERVATION_STATUS ON RESERVATION_STATUS_HISTORY.rsid = RESERVATION_STATUS.id) 
    INNER JOIN ROOM 
    ON RESERVATION_ROOM.rnum = ROOM.number  
    INNER JOIN HOTEL  ON ROOM.hotel_name = HOTEL.hotel_name AND ROOM.hotel_branch = HOTEL.hotel_branch
    WHERE HOTEL.email = '{session_data['email']}';
"""
    #AND RESERVATION_ROOM.isactive = TRUE
    print('HELLO')
    res = execute_sql_query(query=query)
    print(res)
    data = {
        
    }
    print(data.get('ok'))
    for reservation_data in res:
        reservation_id = reservation_data[0]
        reservation_room_number = reservation_data[1]
        reservation_status = reservation_data[2]
        reservation_time = reservation_data[3]
        reservation_time_history = reservation_data[4]
        if data.get(reservation_id) is None:
            print(reservation_id)
            data[reservation_id] = {
                'reservation_id': reservation_id,
                'reservation_room_number':reservation_room_number.split('.')[0],
                'reservation_status':reservation_status,
                'reservation_time':reservation_time,
                'reservation_time_history':reservation_time_history
            }
            print('oke')
        else:
            if data[reservation_id]['reservation_time_history'] <= reservation_time_history:
                data[reservation_id] = {
                    'reservation_id': reservation_id,
                    'reservation_room_number':reservation_room_number.split('.')[0],
                    'reservation_status':reservation_status,
                    'reservation_time':reservation_time,
                    'reservation_time_history':reservation_time_history
                }
        
    data = {
        'reservation' : list(data.values()),
        'is_authorized' : is_authorized,
        'is_hotel': is_authorized
    }
    print(data)

    return render(request=request, template_name='daftar-reservasi-kamar.html', context=data)