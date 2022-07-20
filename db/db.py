import pymysql

conn = pymysql.connect(

    host = "localhost",
    user = "admin",
    password= 'new-strong-password',
    database="test"

)



def create_db ():

    cursor = conn.cursor()
        
    sql_query =  """
    CREATE TABLE book (

    id integer PRIMARY KEY,
    author text NOT NULL,
    language text NOT NULL)
    """

    cursor.execute(sql_query)
    conn.close()

def insert_values ():

    sql_query = "INSERT INTO book(author,language) VALUES (hauuha,huahua)"
    cursor.execute(sql_query)
    conn.close()
