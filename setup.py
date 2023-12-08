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
            SELECT * FROM sistel.user;

""")

# Commit perubahan ke database
conn.commit()
result = cur.fetchall() 
print(result)
# Menutup cursor dan koneksi
cur.close()
conn.close()
