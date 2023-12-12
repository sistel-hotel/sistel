from django.shortcuts import render, redirect
from connect_postgres import execute_sql_query

# Fungsi untuk menampilkan daftar fasilitas hotel
def list_hotel_facilities(request):
    query = "SELECT facility_name, hotel_name, hotel_branch FROM hotel_facilities"
    facilities = execute_sql_query(query)
    return render(request, 'list_facilities.html', {'facilities': facilities})

# Fungsi untuk menambah fasilitas hotel
# views.py

def add_hotel_facility(request):
    if request.method == 'POST':
        facility_name = request.POST.get('facility_name')
        hotel_name = request.POST.get('hotel_name')
        hotel_branch = request.POST.get('hotel_branch')
        
        # Using f-string for the INSERT query
        query = f"INSERT INTO hotel_facilities (facility_name, hotel_name, hotel_branch) VALUES ('{facility_name}', '{hotel_name}', '{hotel_branch}')"
        execute_sql_query(query)
        return redirect('list_hotel_facilities')
    
    return render(request, 'add_facility.html')


# Fungsi untuk mengubah fasilitas hotel
def update_hotel_facility(request, facility_name):
    if request.method == 'POST':
        new_facility_name = request.POST.get('facility_name')
        hotel_name = request.POST.get('hotel_name')
        hotel_branch = request.POST.get('hotel_branch')
        
        query = f"UPDATE hotel_facilities SET facility_name = '{new_facility_name}', hotel_name = '{hotel_name}', hotel_branch = '{hotel_branch}' WHERE facility_name = '{facility_name}'"
        
        execute_sql_query(query)
        return redirect('list_hotel_facilities')
    else:
        query = f"SELECT facility_name, hotel_name, hotel_branch FROM hotel_facilities WHERE facility_name = '{facility_name}'"
        
        # Ensure to fetch the data using fetch=True
        facility = execute_sql_query(query)

        # Check if facility has data before accessing its properties
        if facility:
            return render(request, 'update_facility.html', {'facility': facility[0]})
        else:
            # Handle the case when the facility with the given name is not found
            return HttpResponse("Facility not found", status=404)





# Fungsi untuk menghapus fasilitas hotel
def delete_hotel_facility(request, facility_name, hotel_name, hotel_branch):
    query = f"""DELETE FROM hotel_facilities WHERE facility_name = '{facility_name}' and hotel_name ='{hotel_name}'
    and hotel_branch ='{hotel_branch}'"""
    execute_sql_query(query)
    return redirect('list_hotel_facilities')