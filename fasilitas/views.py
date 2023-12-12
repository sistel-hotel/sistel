from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from connect_postgres import execute_sql_query
from django.views.decorators.csrf import csrf_exempt

# Fungsi untuk menampilkan daftar fasilitas hotel
@csrf_exempt
def list_hotel_facilities(request):
    session_data = request.session.get('user_data')
    print(session_data)
    if not session_data:
        return redirect('/login/')
    is_hotel = session_data['is_hotel']
    query = f"""SELECT facility_name, HOTEL.hotel_name, HOTEL.hotel_branch
      FROM hotel_facilities RIGHT JOIN HOTEL ON HOTEL.hotel_branch = hotel_facilities.hotel_branch 
      AND HOTEL.hotel_name = hotel_facilities.hotel_name WHERE HOTEL.email = '{session_data['email']}';"""
    facilities = execute_sql_query(query)
    return render(request, 'list_facilities.html', {'facilities': facilities, 'is_hotel': is_hotel})


# Fungsi untuk menambah fasilitas hotel
# views.py
@csrf_exempt
def add_hotel_facility(request):
    session_data = request.session.get('user_data')
    print(session_data)
    if not session_data:
        return redirect('/login/')
    is_hotel = session_data['is_hotel']
    if request.method == 'POST':
        facility_name = request.POST.get('facility_name')
        
        query = f"""
        SELECT HOTEL.hotel_name, HOTEL.hotel_branch FROM HOTEL WHERE HOTEL.email = '{session_data['email']}' LIMIT 1;
"""     
        res = execute_sql_query(query=query)

        if len(res) == 0:
            return Http404('Hotel tidak ditemukan')
        hotel_name = res[0][0]
        hotel_branch = res[0][1]
        # Using f-string for the INSERT query
        query = f"""INSERT INTO hotel_facilities 
        (facility_name, hotel_name, hotel_branch) VALUES ('{facility_name}', '{hotel_name}', '{hotel_branch}')
         RETURNING facility_name;"""
        execute_sql_query(query)
        return redirect('list_hotel_facilities')
    
    return render(request, 'add_facility.html', {'is_hotel':is_hotel})


# Fungsi untuk mengubah fasilitas hotel
@csrf_exempt
def update_hotel_facility(request, facility_name):
    session_data = request.session.get('user_data')
    print(session_data)
    if not session_data:
        return redirect('/login/')
    if request.method == 'POST':
        new_facility_name = request.POST.get('facility_name')
        #hotel_name = request.POST.get('hotel_name')
        #hotel_branch = request.POST.get('hotel_branch')

        query = f"""
        SELECT HOTEL.hotel_name, HOTEL.hotel_branch FROM HOTEL WHERE HOTEL.email = '{session_data['email']}' LIMIT 1;
"""     
        res = execute_sql_query(query=query)

        if len(res) == 0:
            return Http404('Hotel tidak ditemukan')
        hotel_name = res[0][0]
        hotel_branch = res[0][1]
        
        query = f"""
        UPDATE hotel_facilities SET facility_name = '{new_facility_name}', hotel_name
          = '{hotel_name}', hotel_branch = '{hotel_branch}' WHERE facility_name = '{facility_name}' AND 
          hotel_name = '{hotel_name}' AND hotel_branch = '{hotel_branch}'
          RETURNING facility_name;
          """
        
        execute_sql_query(query)
        return redirect('list_hotel_facilities')
    else:
        query = f"SELECT facility_name, hotel_name, hotel_branch FROM hotel_facilities WHERE facility_name = '{facility_name}'"
        session_data = request.session.get('user_data')
        print(session_data)
        if not session_data:
            return redirect('/login/')
        
        # Ensure to fetch the data using fetch=True
        facility = execute_sql_query(query)

        # Check if facility has data before accessing its properties
        if len(facility) > 0:
            return render(request, 'update_facility.html', {'facility': facility[0], 'is_hotel': session_data['is_hotel']})
        else:
            # Handle the case when the facility with the given name is not found
            return HttpResponse("Facility not found", status=404)





# Fungsi untuk menghapus fasilitas hotel
@csrf_exempt
def delete_hotel_facility(request, facility_name, hotel_name, hotel_branch):
    query = f"""DELETE FROM hotel_facilities WHERE facility_name = '{facility_name}' and hotel_name ='{hotel_name}'
    and hotel_branch ='{hotel_branch}' RETURNING facility_name;"""
    execute_sql_query(query)
    return redirect('list_hotel_facilities')