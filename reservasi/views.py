from django.shortcuts import render, redirect
from django.http import HttpResponse
from connect_postgres import execute_sql_query


def show_reservasi_kamar(request):
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


def complaint(request, id):
    user_data = request.session['user_data']
    custemail = user_data['email']

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
        """

        execute_sql_query(query=query, fetch_data=False)

        return redirect('reservasi:show-reservasi')

    return HttpResponse("Invalid request method")


def dashboard_pengguna(request):
    user_data = request.session['user_data']
    return render(request, 'dashboard-pengguna.html', {'user_data': user_data})