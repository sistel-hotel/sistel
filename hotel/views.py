from django.shortcuts import render
from connect_postgres import execute_sql_query

# Create your views here.
def dashboard_hotel(request):
    user_data = request.session['user_data']
    email = user_data['email']
    query = f"""
    SELECT * FROM hotel WHERE email = '{ email }'
    """

    hotel_data_dict = None

    res = execute_sql_query(query=query)
    if res:
        keys = [
            'email', 'hotel_name', 'branch_name', 'business_license', 'star_rating',
            'average_rating', 'address', 'area', 'city', 'province', 'description',
            'check_in_time', 'check_out_time'
        ]
        hotel_data_dict = dict(zip(keys, res[0]))
    else:
        print("Hotel data not found")

    hotel_name = hotel_data_dict.get('hotel_name')

    query = f"""
    SELECT * FROM hotel_facilities WHERE hotel_name = '{ hotel_name }'
    """
    
    res = execute_sql_query(query=query)

    facilities = []
    if res:
        keys = [
            'hotel_name', 'branch_name', 'facility_name'
        ]
        for facility in res:
            facilities.append(dict(zip(keys, facility)))
    else:
        print("Hotel facilities data not found")

    query = f"""
    SELECT * FROM room WHERE hotel_name = '{ hotel_name }'
    """
    
    res = execute_sql_query(query=query)

    rooms = []
    if res:
        keys = [
            'hotel_name', 'branch_name', 'number', 'price', 'floor'
        ]
        for facility in res:
            rooms.append(dict(zip(keys, facility)))
    else:
        print("Hotel room data not found")

    return render(request, 'dashboard-hotel.html', { 'user_data': user_data, 'hotel': hotel_data_dict, 'facilities': facilities, 'rooms': rooms })
