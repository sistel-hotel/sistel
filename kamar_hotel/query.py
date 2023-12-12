def sql_get_room(nama_hotel, hotel_branch):
	return f"""
	SELECT R.number, R.price, R.floor, STRING_AGG(RF.ID, ', ') as facilities
    FROM ROOM R
    LEFT JOIN ROOM_FACILITIES RF ON R.number = RF.RNum AND R.hotel_name = RF.hotel_name AND R.hotel_branch = RF.hotel_branch
	WHERE R.hotel_name = '{nama_hotel}' AND R.hotel_branch = '{hotel_branch}'
    GROUP BY R.number, R.price, R.floor;
    """

def sql_insert_room(nomor, harga, lantai, nama_hotel, hotel_branch):
	return f"""
	INSERT INTO
		ROOM(Number, Price, Floor, Hotel_Name, Hotel_Branch)
	VALUES
		(
			'{nomor}',
			'{harga}',
			'{lantai}',
			'{nama_hotel}',
			'{hotel_branch}'
		) RETURNING NUMBER;
	"""

def sql_delete_room(nomor, nama_hotel, hotel_branch):
	return f"""
	DELETE FROM ROOM
	WHERE number = '{nomor}' AND hotel_name = '{nama_hotel}' AND hotel_branch = '{hotel_branch}' RETURNING number;
	"""

def sql_update_room(nomor, harga, lantai, nama_hotel, hotel_branch):
	return f"""
	UPDATE ROOM
	SET price = '{harga}', lantai = '{lantai}'
	WHERE number = '{nomor} AND hotel_name = '{nama_hotel}' AND hotel_branch = '{hotel_branch}'
	returning number;
	"""

def sql_get_nama_branch_hotel(emailuser):
	return f"""
	SELECT hotel_name, hotel_branch
	FROM HOTEL
	WHERE email = '{emailuser}';
	"""