from ast import Global
from multiprocessing.sharedctypes import Value
from flask import Flask, request, jsonify
import pymysql
import pytz
from datetime import datetime
from config import *
from db import db_functions
from flask_cors import CORS,cross_origin
from flask_restx import Resource, Api, fields
from outlier_indentifier_model.generate_data import *
from outlier_indentifier_model.generate_grouped_data import *

import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split

app = Flask(__name__)
api = Api(app)
CORS(app)


global outlier_model

insert_user_data = api.model(
    "Insert_user_data",
    {
        "id": fields.Integer(description="User ID", required=True),
        "outlier_prob": fields.Float(description="Outlier Probability", required=True),
        "class_pred": fields.String(description="Predicted class", required=True),
        "project_name": fields.String( required=True),
        "table_name": fields.String( required=True),
    },
) 



connection_database = api.model(
    "connection_database",
    {

        "project_name": fields.String( required=True),
        "table_name": fields.String( required=True)
    },
) 



@api.route("/insert")
class database(Resource):
    @api.expect(insert_user_data)
    def post(self):
        """insert data"""
        input_json = request.get_json(force=True) 
        
        db_functions.create_table_ifnot_exists(connection_settings,
                                        input_json["project_name"],
                                        input_json["table_name"])
        
        db_functions.insert_data(connection_settings,
                            input_json["id"],
                            input_json["outlier_prob"],
                            input_json["class_pred"],
                            input_json["project_name"],
                            input_json["table_name"])




        return "values inserted"



@api.route("/populate_data")
class database(Resource):
    @api.expect(connection_database)
    def post(self):

        # get connection data
        input_json = request.get_json(force=True) 

        # generate base

        users_table = generate_users()  
        gas_stations_table = generate_gas_stations()
        transactions_table = generate_transactions(users_table, gas_stations_table)
        

        users_table_values =  users_table["data"]
        users_table_values.insert(0, users_table["header"])
        users_table = users_table_values



        gas_stations_table_values =  gas_stations_table["data"]
        gas_stations_table_values.insert(0, gas_stations_table["header"])
        gas_stations_table = gas_stations_table_values


        transactions_table_values =  transactions_table["data"]
        transactions_table_values.insert(0, transactions_table["header"])
        transactions_table = transactions_table_values

        # group the database

        tb_joined_transactions_gas = left_join_arrays(lft_table = transactions_table.copy(),rght_table = gas_stations_table.copy(),key = 'gas_station_id')
        tb_final = left_join_arrays(lft_table =tb_joined_transactions_gas.copy(),rght_table = users_table.copy(),key = 'user_id')
        tb_array = np.array(tb_final)
        table_grouped = group_values(table_array = tb_array)   
        table_grouped = np.array(table_grouped['data'])
        
        user_ids = table_grouped[1:,0]
        X = table_grouped[1:,1:].astype(float)
        
        
        # Split data to train the model 

        X_train, X_test, users_train, users_test = train_test_split(X, user_ids, test_size=0.5, random_state=42)


        # Model

        clf = IsolationForest(random_state=0).fit(X_train)

        predictions = clf.predict(X_test)
        scores = clf.score_samples(X_test)*-1

        predictions_classes = []

        for i in predictions:    
            
            if i == 1:
            
                predictions_classes.append("nonfraud")
            
            else:
                predictions_classes.append("fraud")


        # Insert data into database

        db_functions.create_table_ifnot_exists(connection_settings,
                                        input_json["project_name"],
                                        input_json["table_name"])
        
        db_functions.insert_data(connection_settings,
                            users_test.tolist(),
                            scores.tolist(),
                            predictions_classes,
                            input_json["project_name"],
                            input_json["table_name"])

        
        outlier_model = clf

        
        return "database populated and model trained"






# @app.route('/insert', methods=["POST"])
# @cross_origin()
# def insert_score():

#     input_json = request.get_json(force=True) 
     
#     db_functions.create_table_ifnot_exists(connection_settings,
#                                       input_json["project_name"],
#                                       input_json["table_name"])
    
#     db_functions.insert_data(connection_settings,
#                         input_json["id"],
#                         input_json["outlier_prob"],
#                         input_json["class_pred"],
#                         input_json["project_name"],
#                         input_json["table_name"])




#     return "values inserted"

if __name__ == '__main__':

    app.run(host='0.0.0.0')