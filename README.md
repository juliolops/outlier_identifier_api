# outlier_identifier_api

## Abstract

This project is a API to populate a MySQL database with fraud scores of the clients. This API was developed in Python language with Flask web framework and It is containerized so that it is runned using docker-compose up command. The chosen machine learning model to identify the outliers is a Isolation Forest.

---

## Tecnologies

- Flask
- MySQL
- Docker

---

## Command to Execute all aplication

```docker-compose up command```

---

## Endpoint to insert values into project_name.table_name

```http://0.0.0.0:5000/insert```

This route receive post requests and the data has the following fields: id(user id primary key), outlier_prob, class_pred (fraud or nonfraud), project_name and table_name. The data received is persisted in the table called project_name.table_name.


```
Example of post request to insert one value

{
    
    "id":12,
    "outlier_prob":0.2,
    "class_pred":"nonfraud",
    "project_name":"raizen_gasoline",
    "table_name":"fraud"
    
}

```

```
Example of post request to insert many values

{
    
    "id":[12,14,17,30],
    "outlier_prob":[0.2,0.7,0.8,0.3],
    "class_pred":["nonfraud","fraud","fraud","nonfraud"],
    "project_name":"raizen_gasoline",
    "table_name":"fraud"
    
}

```
---
# Development of machine learning model to identify outliers 



## The path of the **Jupyter notebook** used for model development is:

```/outlier_indentify_model/outlier_model_development.ipynb```

## Script in **outlier_model_development.ipynb** to train the model:

```
from sklearn.ensemble import IsolationForest
 
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




## The path of the **script** used for generate the features **total_liters, total_amount_paid and is_premium** is:

```/outlier_indentify_model/generate_grouped_data.py```



## Command to generate the ML table called **group_data_by_users.csv**

```python generate_grouped_data.py``` 

---

## Dependencies 

requirements.txt has all the dependencies of this aplication

