from django.shortcuts import render, redirect
from django.http import HttpResponse
from connect_postgres import execute_sql_query
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def show_reservasi_kamar(request):
    user_data = request.session['user_data']
    
    if not user_data:
        return redirect('/login/')
    custemail = request.session['user_data']['email']
    query = f""" 
                SELECT rr.rsv_id, rr.rNum, rr.rhotelname, rr.rhotelbranch, rr.Datetime, rr.isActive
                FROM reservation r
                JOIN reservation_room rr ON r.rID = rr.rsv_id
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