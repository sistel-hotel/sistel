import psycopg2

def execute_sql_query(query):
        connection = psycopg2.connect(
            dbname='sistelproject_dayablewhy', 
            user='sistelproject_dayablewhy', 
            password='15eaebb5beb4f3e1c03e5b1e708da41579aaef3f', 
            host='eum.h.filess.io', 
            port='5432'
        )
        cursor = connection.cursor()
        cursor.execute("SET search_path TO sistel")
        cursor.execute(query)
        connection.commit()

        result = cursor.fetchall() 

        cursor.close()
        connection.close()

        return result 
  
