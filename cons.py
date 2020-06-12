#Importing necessary modules
import os
os.environ["PYSPARK_PYTHON"]='/usr/bin/python3'
from time import sleep
from datetime import datetime
from kafka import KafkaConsumer
import pandas as pd
import json

#Importing pyspark modules
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegressionModel


#Declearing spark context
sc= SparkContext()
sqlContext = SQLContext(sc)

#Declearing the model path
try:
    Path = "StockPricepred_Model"
    load_model = LinearRegressionModel.load(Path)
except:
    print("Decleared wrong path")

#Declearing consumer connection
try:
    consumer = KafkaConsumer('stock_prices',bootstrap_servers=['localhost:9092'])
except:
    print('connection error')

#getting data and predicting result using the model
def stock_prediction(load_model):
        try:
            for msg in consumer:
                res = json.loads(msg.value.decode('utf-8'))
                dlist = list(res.values())
                df = pd.DataFrame([dlist], columns=['Open', 'Close', 'Volume', 'High', 'Low'])
                df = df.astype(float)
                spark_df = sqlContext.createDataFrame(df)
                vectorAssembler = VectorAssembler(inputCols=['Open', 'High', 'Low'], outputCol='features')
                df_vect = vectorAssembler.transform(spark_df)
                df_vect_features = df_vect.select(['features', 'Close'])
                predictions = load_model.transform(df_vect_features)
                predictions.select("prediction", "Close", "features").show()
                predict_value = predictions.select('prediction').collect()[0].__getitem__("prediction")
                close_value = predictions.select('Close').collect()[0].__getitem__('Close')
                print(msg.key)
                date_time = msg.key.decode('utf-8')
                return predict_value, close_value, date_time
        except:
            print('Debug the above lines of code')
stock_prediction(load_model)





