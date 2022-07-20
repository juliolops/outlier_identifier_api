import csv
import numpy as np


#Load Generated Data

def load_data():

    with open("gas_stations.csv", "r") as csvfile:
        reader_variable = csv.reader(csvfile, delimiter=",")

        gas_stations_table = [row for row in reader_variable]

    with open("transactions.csv", "r") as csvfile:
        reader_variable = csv.reader(csvfile, delimiter=",")

        transactions_table = [row for row in reader_variable]
        
    with open("users.csv", "r") as csvfile:
        reader_variable = csv.reader(csvfile, delimiter=",")

        users_table = [row for row in reader_variable]

    return gas_stations_table, transactions_table, users_table

#Join data

def left_join_arrays(lft_table,rght_table,key):
    
    
    map_lft_columns = {}

    for i,j in enumerate(lft_table[0]):
        map_lft_columns[j] = i


    map_rght_columns = {}

    for i,j in enumerate(rght_table[0]):
        map_rght_columns[j] = i


        
    for lft_iterator,lft_column in enumerate(lft_table[1:]):


        for rght_iterator,rght_column in enumerate(rght_table[1:]):


            if lft_column[map_lft_columns[key]] == rght_column[map_rght_columns[key]]:


                lft_table[lft_iterator+1] = lft_table[lft_iterator+1]+rght_table[rght_iterator+1][0:map_rght_columns[key]]+rght_table[rght_iterator+1][map_rght_columns[key]+1:]

    lft_table[0] = lft_table[0]+rght_table[0][0:map_rght_columns[key]]+rght_table[0][map_rght_columns[key]+1:]
    
    return lft_table


# Group by values

def group_values(table_array):

    table_grouped = [["user_id","total_liters","total_amount_paid","is_premium"]]


    for iterator_val in np.unique(table_array[1:,1]):
        
        list_values = []
        
        sum_values = np.sum(table_array[table_array[:,1]==str(iterator_val)].astype("float"),axis=0)
            
        max_values = np.max(table_array[table_array[:,1]==str(iterator_val)].astype("float"),axis=0)
        
        list_values = [iterator_val,sum_values[3],sum_values[4],int(max_values[5])]
        
        table_grouped.append(list_values)

    return {'header': table_grouped[0], 'data': table_grouped[1:]}


def write_data(out, header, data):
    try:
        with open(out, 'w', newline='') as f:
          writer = csv.writer(f)
          writer.writerow(header)
          writer.writerows(data)
    except Exception as err:
        print('Failed to write %s' % out)



if __name__ == '__main__':
    
    
    gas_stations_table, transactions_table, users_table = load_data()
    
    tb_joined_transactions_gas = left_join_arrays(lft_table = transactions_table.copy(),rght_table = gas_stations_table.copy(),key = 'gas_station_id')
    
    tb_final = left_join_arrays(lft_table =tb_joined_transactions_gas.copy(),rght_table = users_table.copy(),key = 'user_id')
    
    tb_array = np.array(tb_final)
    
    table_grouped = group_values(table_array = tb_array)
    
    write_data('group_data_by_users.csv', table_grouped['header'], table_grouped['data'])