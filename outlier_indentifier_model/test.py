import csv
import numpy as np
import requests


data_scores = {"id":5617561561,
               "outlier_prob":1,
               "class_pred":"n",
               "project_name":"outliers_db",
               "table_name":"fraud"}



url = "http://0.0.0.0:5000/insert"

response = requests.post(url, data_scores)
print(response)