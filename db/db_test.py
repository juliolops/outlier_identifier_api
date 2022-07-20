import pymysql
from datetime import datetime
import pytz

def insert_data(connection_settings,user_id,outlier_prob,class_pred,project_name,table_name):

    conn = pymysql.connect(

        host = connection_settings["host"],
        user = connection_settings["user"],
        password= connection_settings['password'],
        #database=connection_settings["database"]
        database=project_name
    )

    now = datetime.now(pytz.timezone('Brazil/East'))
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
     
    cursor = conn.cursor()
    sql_query = "INSERT INTO {}(time,id,outlier_prob,class_pred) VALUES (%s,%s,%s,%s)".format(table_name)
    
       
    if isinstance(outlier_prob, list) and isinstance(user_id, list) and isinstance(class_pred, list):

        data = [[formatted_date,i,j,z] for i,j,z in zip(user_id,outlier_prob,class_pred)]
        cursor.executemany(sql_query,data)
    
    else:

        cursor.execute(sql_query,(formatted_date,str(user_id),str(outlier_prob),str(class_pred)))


    conn.commit()
    conn.close()



def create_table_ifnot_exists(connection_settings,project_name,table_name):

    conn = pymysql.connect(

        host = connection_settings["host"],
        user = connection_settings["user"],
        password= connection_settings['password'],
        database=project_name

    )

    
    cursor = conn.cursor()
        
    sql_query =  """
    CREATE TABLE IF NOT EXISTS {} (

    id int(11) PRIMARY KEY NOT NULL,
    time timestamp NOT NULL,
    outlier_prob float NOT NULL,
    class_pred VARCHAR(20) NOT NULL

    )
    """.format(table_name)

    cursor.execute(sql_query)
    conn.close()
