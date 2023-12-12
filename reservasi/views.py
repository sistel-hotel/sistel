import random
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from connect_postgres import execute_sql_query, execute_sql_query_no_fetch
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def show_reservasi_kamar(request):
    user_data = request.session['user_data']
    
    if not user_data:
        return redirect('/login/')
    custemail = request.session['user_data']['email']
    query = f""" 
                SELECT rr.rsv_id, rr.rNum, rr.rhotelname, rr.rhotelbranch, rr.Datetime, rr.isActive, rs.status
                FROM reservation r
                JOIN reservation_room rr ON r.rID = rr.rsv_id
                JOIN reservation_status rs ON r.rID = rs.id
                WHERE r.cust_email = '{custemail}'
                """
    res = execute_sql_query(query=query)

    data = []
    for row in res:
        data.append({
            'rsv_id': row[0],
            'rnum': row[1],
            'rhotelname': row[2],
            'rhotelbranch': row[3],
            'Datetime': row[4],
            'isActive': row[5],
            'status': row[6],
        })
    print(data)
    context = {
        "data": data,
    }
    return render(request, "daftar-reservasi-kamar.html", context)

@csrf_exempt
def complaint(request, id):
    user_data = request.session['user_data']
    custemail = user_data['email']
    if not user_data:
        return redirect('/login/')

    query = f"""
        SELECT rr.rsv_id, rr.rNum, rr.rhotelname, rr.rhotelbranch
        FROM reservation r
        JOIN reservation_room rr ON r.rID = rr.rsv_id
        WHERE r.cust_email = '{custemail}' AND r.rID = '{id}'
    """

    res = execute_sql_query(query=query)

    if len(res) > 0:
        row = res[0]
        data = {
            'rsv_id': row[0],
            'rnum': row[1],
            'rhotelname': row[2],
            'rhotelbranch': row[3],
        }

    context = {
        'id': id,
        'data': data,
        'user_data': {
            'email': user_data['email'],
            'name': user_data['fname'] + " " + user_data['lname']
        }
    }
    print(context)
    return render(request, "complaint-reservasi.html", context)

@csrf_exempt
def save_complaint(request, id):
    def increment_string(id):

        letter_part = ''.join(filter(str.isalpha, id))
        number_part = ''.join(filter(str.isdigit, id))

        incremented_number = str(int(number_part) + 1)

        result_string = letter_part + incremented_number

        return result_string
    
    if request.method == 'POST':

        complaint_message = request.POST.get('complaintMessage')
        email = request.POST.get('email')

        query_latest_id = f"""
        SELECT * FROM complaints ORDER BY id DESC LIMIT 1
        """

        res = execute_sql_query(query=query_latest_id)

        latest_complaint_id = increment_string(res[0][0])

        query = f"""
            INSERT INTO complaints (id, cust_email, rv_id, complaint)
            VALUES ('{latest_complaint_id}', '{email}', '{id}', '{complaint_message}')
            RETURNING id;
        """

        execute_sql_query(query=query)

        return redirect('reservasi:show-reservasi')

    return HttpResponse("Invalid request method")

@csrf_exempt
def dashboard_pengguna(request):
    user_data = request.session['user_data']
    if not user_data:
        return redirect('/login/')
    query = f"""
    SELECT CUSTOMER.nik, RESERVATION_ACTOR.phonenum FROM CUSTOMER LEFT JOIN  RESERVATION_ACTOR ON
    CUSTOMER.email = RESERVATION_ACTOR.email
    WHERE CUSTOMER.email = '{user_data['email']}' LIMIT 1;
    """
    res = execute_sql_query(query=query)
    res = res[0]
    nik = res[0]
    phonenum = res[1]    
    query_recent_comments = f"""
    SELECT DISTINCT review, hotel_name, hotel_branch, rating FROM REVIEWS WHERE cust_email = '{user_data['email']}';
"""
    res_comment = execute_sql_query(query_recent_comments)
    comments = []
    complaints = []
    query_complaints = f"""
    SELECT DISTINCT COMPLAINTS.complaint, RESERVATION_ROOM.rhotelname, RESERVATION_ROOM.rhotelbranch
    , RESERVATION_ROOM.rnum
    FROM COMPLAINTS INNER JOIN RESERVATION_ROOM ON COMPLAINTS.rv_id = RESERVATION_ROOM.rsv_id 
    WHERE COMPLAINTS.cust_email = '{user_data['email']}';
"""
    res_complaints = execute_sql_query(query_complaints)
    for complaint in res_complaints:
        complaints.append(
            {
                'text': complaint[0],
                'hotel_name': complaint[1],
                'hotel_branch': complaint[2],
                'room_number': complaint[3].split('.')[0]
            }
        )
    for comment in res_comment:
        comments.append(
            {
                'text': comment[0],
                'hotel_name': comment[1],
                'hotel_branch': comment[2],
                'rating': comment[3]
            }
        )
    return render(request, 'dashboard-pengguna.html', 
                  {'user_data': user_data, 'nik':nik, 'phone':phonenum, 
                                                      'complaints':complaints ,'comments':comments})


def buat_reservasi(request):
    def generate_random_string(length):
        random_string = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz', k=length))
        return random_string
    
    def generate_payment_id():
        part1 = ''.join(random.choices('0123456789', k=3))
        part2 = ''.join(random.choices('0123456789', k=2))
        part3 = ''.join(random.choices('0123456789', k=4))
        random_string = f"{part1}-{part2}-{part3}"
        return random_string
    
    if request.method == 'POST':

        user_data = request.session['user_data']
        email = user_data['email']

        hotel_name = request.POST.get('hotel_name')
        hotel_branch = request.POST.get('hotel_branch')
        number = request.POST.get('number')

        checkin = request.POST.get('start-date')
        checkout = request.POST.get('end-date')
        payment_option = request.POST.get('payment-option')
        payment = request.POST.get('payment')
        payment_id = generate_payment_id()

        create_payment = execute_sql_query_no_fetch(f"""
        INSERT INTO payment (payment_id, status) VALUES ('{payment_id}', 'pending')
        """)

        payment_query = ""
        if payment_option == 'kredit':
            payment_query += f"""
            INSERT INTO kredit (no_kartu, payment_id) VALUES ('{payment}', '{payment_id}')
            """
        elif payment_option == 'debit':
            payment_query += f"""
            INSERT INTO debit (no_rekening, payment_id) VALUES ('{payment}', '{payment_id}')
            """
        elif payment_option == 'ewallet':
            payment_query += f"""
            INSERT INTO ewallet (phone_num, payment_id) VALUES ('{payment}', '{payment_id}')
            """

        create_payment_method = execute_sql_query_no_fetch(payment_query)

        rid = generate_random_string(20)

        hotel = execute_sql_query(f"""
        SELECT * FROM room WHERE 
        hotel_name = '{hotel_name}' AND 
        hotel_branch = '{hotel_branch}' AND 
        number = '{number}.0'
        """)

        hotel = hotel[0]

        reservation_query = execute_sql_query_no_fetch(f"""
        INSERT INTO reservation (rid, total_price, checkin, checkout, payment, cust_email)
        VALUES('{rid}', '{hotel[3]}', '{checkin}', '{checkout}', '{payment_id}', '{email}')
        """)

        reservation_status_query = execute_sql_query_no_fetch(f"""
        INSERT INTO reservation_status (id, status)
        VALUES('{rid}', 'Menunggu Konfirmasi Pihak Hotel')
        """)

        date = datetime.today().strftime('%Y-%m-%d')

        reservation_room_query = execute_sql_query_no_fetch(f"""
        INSERT INTO reservation_room (rsv_id, rnum, rhotelname, rhotelbranch, datetime, isactive)
        VALUES('{rid}', '{number}.0', '{hotel_name}', '{hotel_branch}', '{date}', 'false')
        """)

        print(reservation_room_query)

        return redirect('reservasi:show-reservasi')
    else:
        return render(request, 'buat-reservasi.html')
    

def detail_reservasi(request, id):
    room_query = execute_sql_query(f"""
    SELECT * FROM reservation_room
    WHERE rsv_id = '{id}'
    """)

    hotel = room_query[0]

    hotel_data = {
        'id': hotel[0],
        'room_number': hotel[1],
        'hotel_name': hotel[2],
        'hotel_branch': hotel[3],
        'date': hotel[4],
        'status': hotel[5],
    }

    shuttle_query = execute_sql_query(f"""
    SELECT * FROM reservation_shuttleservice
    WHERE rsv_id = '{id}'
    """)

    shuttle_data = {}
    if(shuttle_query):
        shuttle = shuttle_query[0]

        shuttle_data = {
            'id': shuttle[0],
            'vehicle_num': shuttle[1],
            'driver_phonenum': shuttle[2],
            'date': shuttle[3],
            'status': shuttle[4],
        }

    context = {
        'room': hotel_data,
        'shuttle': shuttle_data
    }

    print(context)

    return render(request, 'detail-reservasi.html', context)

def cancel_reservasi(request, id):
    update_status = execute_sql_query_no_fetch(f"""
    UPDATE  reservation_status SET status = 'Dibatalkan Customer' WHERE id = '{id}'
    """)

    return redirect('reservasi:show-reservasi')

