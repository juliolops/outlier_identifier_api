# outlier_identifier_api

## Abstract

This project is a API to populate a MySQL database with fraud scores of the clients. This API was developed in Python language with Flask web framework and It is containerized so that it is runned using docker-compose up command. The chosen machine learning model to identify the outliers is a Isolation Forest. This application is documented by swagger so it is possible for the user to manipulate the api using the swagger UI.

---

## Swagger UI

![image](https://user-images.githubusercontent.com/40969977/180535343-3962d8e4-c3da-4577-a98f-a909105ec3b0.png)

---

## Tecnologies

- Flask
- MySQL
- Docker

---

## Command to Execute all aplication

```docker-compose up command```

---

## Endpoint to insert values into project_name.table_name (POST)

```http://0.0.0.0:5000/insert```

This route receive post requests and the data has the following fields: id(user id), outlier_prob, class_pred (fraud or nonfraud), project_name and table_name. The data received is persisted in the table called project_name.table_name.


```
Example of json to insert one value

{
    
    "id":12,
    "outlier_prob":0.2,
    "class_pred":"nonfraud",
    "project_name":"raizen_gasoline",
    "table_name":"fraud"
    
}

```

```
Example of json to insert many values

{
    
    "id":[12,14,17,30],
    "outlier_prob":[0.2,0.7,0.8,0.3],
    "class_pred":["nonfraud","fraud","fraud","nonfraud"],
    "project_name":"raizen_gasoline",
    "table_name":"fraud"
    
}

```
---

## Endpoint to populate the database with scores (POST)

```http://0.0.0.0:5000/populate_data```

This route generate the database and process it for calculate the prediction variables (total_liters, total_amount_paid and is_premium), train the machine learning model then persist that into database.


```
Example of json to populate the database

{

    "project_name":"raizen_gasoline",
    "table_name":"fraud"
    
}

```

## Endpoint to train the machine learning model (GET)

```http://0.0.0.0:5000/train```

This route receive **get request** and generate the database and process it for calculate the predictions variables (total_liters, total_amount_paid and is_premium) then train the machine learning model



## Endpoint to predict the score (POST)

```http://0.0.0.0:5000/predict```

This route predict the score with trained model


```
Example of json to predict scores

{
  "total_liters": 100,
  "total_amount_paid": 100,
  "is_premium": 1
}

```
---
# Tests

The python file called **test_api.py** in the root directory has 4 aplication tests (one for each route). These tests are executed by the **library pytest** using the command **py.test**. You have to run **py.test** in the root directory. 

---
# Development of machine learning model to identify outliers 



## The path of the **Jupyter notebook** used for model development is:

```/outlier_indentify_model/outlier_model_development.ipynb```

## Script in **outlier_model_development.ipynb** to train the model:

```
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
 
table_grouped_array = np.array(table_grouped)
user_ids = table_grouped_array[1:,0]
X = table_grouped_array[1:,1:].astype(float)


X_train, X_test, users_train, users_test = train_test_split(X, user_ids, test_size=0.5, random_state=42)

clf = IsolationForest(random_state=0).fit(X_train)

predictions = clf.predict(X_test)
scores = clf.score_samples(X_test)*-1

predictions_classes = []

for i in predictions:    
    if i == 1:
        predictions_classes.append("nonfraud")
    else:
        predictions_classes.append("fraud")

```


## Script in **outlier_model_development.ipynb** to populate the database with the predictions:

```
data_scores = {"id":users_test.tolist(),
               "outlier_prob":scores.tolist(),
               "class_pred":predictions_classes,
               "project_name":"raizen_gasoline",
               "table_name":"fraud"}


url = "http://0.0.0.0:5000/insert"

response = requests.post(url, json=data_scores)
print(response)

```

## Histogram of the prediction variables by predicted class applied in the test dataset:

![download](https://user-images.githubusercontent.com/40969977/180610893-14a444e5-06e5-4e0a-b64b-411122966bd5.png)

## Boxplots of the prediction variables by predicted class applied in the test dataset:

![download (1)](https://user-images.githubusercontent.com/40969977/180611001-a54b30a6-3dcd-4fd3-886d-61d669313e9e.png)


## Some observations about the results of the model in the test dataset

- the median, maximum and minimum of the variables total_amout_paid and total_liters for customers predicted as fraud are quite discrepant when compared to customers predicted as not fraud, as we can see in the boxplots.



- The distributions of variables total liters, total amount of customers predicted as non-fraudulent have the shape of a normal distribution, whereas customers predicted as fraudulent have distributions well distributed in small and high values.


- the model is considering all premiuns as fraud, as we can see in the histogram above, but considering that the model identifies outliers and premium customers are exclusive and have a specific behavior, this is expected to happen because it is quite different from most other customers. A possible treatment for version 2 of this model is to create a segmentation for these premium customers.



## The path of the **script** used for generate the features **total_liters, total_amount_paid and is_premium** is:

```/outlier_indentify_model/generate_grouped_data.py```



## Command to generate the ML table called **group_data_by_users.csv**

```python generate_grouped_data.py``` 

---

## Dependencies 

requirements.txt has all the dependencies of this aplication

