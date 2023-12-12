from kamar_hotel.query import *
from django.shortcuts import render, redirect, HttpResponseRedirect
from connect_postgres import execute_sql_query
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from sistel.helper.function import *
from django.db import connection, InternalError


# Create your views here.
def get_nama_branch_hotel(request):
	cursor = connection.cursor()
	cursor.execute("SET SEARCH_PATH TO SISTEL;")

	userData = request.session.get('user_data')
	email_user = userData['email']
 	
	query = sql_get_nama_branch_hotel(email_user)
	cursor.execute(query)
	data = parse(cursor)
	data_hotel = data[0]

	hotel_name = data_hotel['hotel_name']
	hotel_branch = data_hotel['hotel_branch']

	return hotel_name, hotel_branch

def kamar_hotel(request):
	nama_hotel, hotel_branch = get_nama_branch_hotel(request)

	context = {}
	cursor = connection.cursor()
	cursor.execute("SET SEARCH_PATH TO SISTEL;")

	query = sql_get_room(nama_hotel, hotel_branch)
	cursor.execute(query)
	data = parse(cursor)
	daftar_kamar = []
	for kamar in data:
		kamar['slug'] = title_to_slug(kamar['number'])
		daftar_kamar.append(kamar)
	context['data_kamar'] = daftar_kamar

	return render(request, "kamarhotel.html", context)

def show_create_kamar_hotel(request):
	context = {}
	if request.method == 'POST':
		if 'submitKamar' in request.POST:
			nomor = request.POST.get('nomor')
			harga = request.POST.get('price')
			lantai = request.POST.get('lantai')
			data = create_kamar_hotel(request, nomor, harga, lantai)
			if data['success']:
				return redirect('kamar_hotel:kamar_hotel')
			else:
				context['message'] = parse_error_message(data['msg'])
	return render(request, "show_create_kamar_hotel.html", context)

def create_kamar_hotel(request, nomor, harga, lantai):
	nama_hotel, hotel_branch = get_nama_branch_hotel(request)

	context = {}
	cursor = connection.cursor()
	cursor.execute("SET SEARCH_PATH TO SISTEL;")

	try:
		query = sql_insert_room(nomor, harga, lantai, nama_hotel, hotel_branch)
		cursor.execute(query)
	except InternalError as e:
		message = str(e)
		return {
			'success' : False,
			'msg' : message
		}
	else:
		return {
			'success' : True
		}
		
def delete_kamar_hotel(request, kamar):
	nama_hotel, hotel_branch = get_nama_branch_hotel(request)

	context = {}
	cursor = connection.cursor()
	cursor.execute("SET SEARCH_PATH TO SISTEL;")

	nomor = slug_to_title(kamar)

	query = sql_delete_room(nomor, nama_hotel, hotel_branch)
	try:
		cursor.execute(query)
	except Exception as e:
		return {
			'success' : False,
			'msg' : message
		}
	else:
		return {
			'success' : True
		}