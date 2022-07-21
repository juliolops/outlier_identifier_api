from flask import Flask, request, jsonify
import pymysql
import pytz
from datetime import datetime
from config import *
from db import db_functions
from flask_cors import CORS,cross_origin


app = Flask(__name__)
CORS(app)


@app.route('/insert', methods=["POST"])
@cross_origin()
def insert_score():

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

if __name__ == '__main__':

    app.run(host='0.0.0.0')