# Copyright 2021 Raizen Analytics

import numpy
import csv


def add_ouliter_consumption():
    if numpy.random.uniform() > 0.98:
        return numpy.random.randint(500, 800)
    return 0


def add_outlier_price():
    if numpy.random.uniform() > 0.98:
        return numpy.random.randint(15, 20)
    return 0


def generate_transactions(users, gas_stations):
    num_transactions = 100000
    num_users = len(users['data'])
    num_gas_stations = len(gas_stations['data'])

    header = [
        'transaction_id',
        'user_id',
        'gas_station_id',
        'liters'
    ]

    data = [[
        i,
        users['data'][numpy.random.randint(0, num_users)][0],
        gas_stations['data'][numpy.random.randint(0, num_gas_stations)][0],
        int(numpy.random.normal(70, 20)) + add_ouliter_consumption()
    ] for i in range(num_transactions)]

    return {'header': header, 'data': data}


def generate_gas_stations():
    num_gas_stations = 50
    header = [
        'gas_station_id',
        'gasoline_price_per_litre'
    ]

    data = [[
        i,
        numpy.random.normal(5.213, 1.34) + add_outlier_price()
    ] for i in range(num_gas_stations)]

    return {'header': header, 'data': data}


def generate_users():
    num_users = 10000
    header = [
        'user_id',
        'is_premium'
    ]

    data = [[
        i,
        1 if numpy.random.uniform() > 0.95 else 0
    ] for i in range(num_users)]

    return {'header': header, 'data': data}


def write_data(out, header, data):
    try:
        with open(out, 'w', newline='') as f:
          writer = csv.writer(f)
          writer.writerow(header)
          writer.writerows(data)
    except Exception as err:
        print('Failed to write %s' % out)


if __name__ == '__main__':
    users = generate_users()
    gas_stations = generate_gas_stations()
    transactions = generate_transactions(users, gas_stations)

    write_data('users.csv', users['header'], users['data'])
    write_data('gas_stations.csv', gas_stations['header'], gas_stations['data'])
    write_data('transactions.csv', transactions['header'], transactions['data'])