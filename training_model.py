import boto3
import pandas as pd
#creating client obj for s3

client=boto3.client('s3')

path = 's3://phani06062020/stockData1.csv'
df = pd.read_csv(path)
print(df.head())

# # EXPLORATORY DATA ANALYSIS
print(df.count())
print(df.dtypes)
print(df.info())
df['Date'] = pd.to_datetime(df.Date)
df['Date'] = df['Date'].dt.strftime('%m/%d/%Y')
print(df['Date'])

print(df.columns.tolist())

#Renaming columns
df = df.rename(columns={df.columns[1] : 'Close'})
df = df.rename(columns={df.columns[3] : 'Open'})
df = df.rename(columns={df.columns[4] : 'High'})
df = df.rename(columns={df.columns[5] : 'Low'})
df = df.rename(columns={df.columns[2] : 'Volume'})
#Converting the string columns to float values
df['Close'] = df['Close'].str.replace(',','').str.replace('$','').astype('float')
df['Open'] = df['Open'].str.replace(',','').str.replace('$','').astype('float')
df['High'] = df['High'].str.replace(',','').str.replace('$','').astype('float')
df['Low'] = df['Low'].str.replace(',','').str.replace('$','').astype('float')
print(df.dtypes)
#printing top  5 rows
print(df.head())
#Discriptive statistics of dataset 
print(df.describe())

#Checking null values

try:
    print(df.isnull().sum())
except:
    print("No null values in dataset")

#finding correlation function
print(df.corr())

#

#Importing spark modules
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext
sc= SparkContext()
sqlContext = SQLContext(sc)

data = sqlContext.createDataFrame(df)

print(data.show())

print(data.printSchema())

#Importing linear regression from pyspark mllib
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

from pyspark.ml.linalg import Vectors
from pyspark.ml.feature import VectorAssembler
#Converting the three independent variables into single column features 
#using vector assembler
featureassembler=VectorAssembler(inputCols=["Open","High","Low"],outputCol="Features")

output=featureassembler.transform(data)

print(output.show())

finalized_data = output.select("features","Close")

print(finalized_data.show())
#spliting the dataset in ratio 8:2 
train_data,test_data=finalized_data.randomSplit([0.80,0.20])
#training the model
regressor=LinearRegression(featuresCol='features', labelCol='Close')
regressor=regressor.fit(train_data)
#Finding  coefficients 
print(regressor.coefficients)
#finding intercept
print(regressor.intercept)

pred_results=regressor.evaluate(test_data)

print(pred_results.predictions.show())

from pyspark.ml.evaluation import RegressionEvaluator
#Finding coefficient of determination and  rsme values
try :
    # training Summary
    trainingSummary=regressor.summary
    print("RMSE: %f"%trainingSummary.rootMeanSquaredError)
    print("r2: %f" % trainingSummary.r2)
except:
    print(" Model Test have a Problem")

#saving the model
regressor.save("StockPricepred_Model")
print("Succesfully Saved")


#import pickle
#Pkl_Filename = "Regressor_Model"
#with open(Pkl_Filename, 'wb') as f:
 #   pickle.dump(regressor, f)
