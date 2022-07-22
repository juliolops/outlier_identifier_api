import requests




def test_post_insert():

     data = {"id": 0,
            "outlier_prob": 0.2,
            "class_pred": "fraud",
            "project_name": "raizen_gasoline",
            "table_name": "fraud"}
     
     response = requests.post("http://0.0.0.0:5000/insert", json=data)

     assert response.status_code == 200

def test_get_train():

     response = requests.get("http://0.0.0.0:5000/train")
    
     assert response.status_code == 200


def test_post_populate_data():

     data = {"project_name": "raizen_gasoline",
            "table_name": "fraud"}
     
     response = requests.post("http://0.0.0.0:5000/populate_data", json=data)

     assert response.status_code == 200

def test_post_predict():

     data = { "total_liters": 0,
              "total_amount_paid": 100,
              "is_premium": 0}
        
     response = requests.post("http://0.0.0.0:5000/predict", json=data)

     assert response.status_code == 200