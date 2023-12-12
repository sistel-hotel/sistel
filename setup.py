import psycopg2

# Koneksi ke database
conn = psycopg2.connect(
    dbname='sistelproject_dayablewhy', user='sistelproject_dayablewhy', password='15eaebb5beb4f3e1c03e5b1e708da41579aaef3f', host='eum.h.filess.io', port='5432'
)

# Membuka file SQL dan membacanya
with open('setup.sql', 'r') as file:
    sql = file.read()

# Membuat cursor
cur = conn.cursor()

# Menjalankan perintah SQL
cur.execute("""
SET SEARCH_PATH to sistel;
CREATE OR REPLACE FUNCTION validate_hotel_reservation_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.rsid NOT IN ('P1Q0R2S3T4U5V6', 'X9Y8Z7W6V5U4T3', 'gVmGZxNrVbOgGTYyhTnb') THEN
        RAISE EXCEPTION 'Pihak Hotel hanya dapat melakukan perubahan status ke ''Ditolak oleh Hotel'' atau ''Terkonfirmasi oleh Hotel''';
    END IF;

    IF  OLD.rsid NOT IN ('A7B1D9E4F2C5G3H0', 'gVmGZxNrVbOgGTYyhTnb', 'XTsJpaMwNMrkpjBNstWY', 'LABduoOaWJlzgCjvIkUY') THEN
        RAISE EXCEPTION 'Hotel hanya dapat mengubah reservasi dengan status ''Menunggu Konfirmasi Pihak Hotel''';
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

""")

# Commit perubahan ke database
conn.commit()
result = cur.fetchall() 
print(result)
# Menutup cursor dan koneksi
cur.close()
conn.close()
