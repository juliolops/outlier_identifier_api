from flask import Flask, request, jsonify
import pymysql
import pytz
from datetime import datetime
from config import *
from db import db_test
from flask_cors import CORS,cross_origin


app = Flask(__name__)
CORS(app)


@app.route('/')
@cross_origin()
def hello_world():
    return 'This is my first API cal!'

@app.route('/insert', methods=["POST"])
@cross_origin()
def insert_score():

    input_json = request.get_json(force=True) 
     
    db_test.create_table_ifnot_exists(connection_settings,
                                      input_json["project_name"],
                                      input_json["table_name"])
    
    db_test.insert_data(connection_settings,
                        input_json["id"],
                        input_json["outlier_prob"],
                        input_json["class_pred"],
                        input_json["project_name"],
                        input_json["table_name"])




    return "values inserted"

if __name__ == '__main__':

    app.run(host='0.0.0.0')