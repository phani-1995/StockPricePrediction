import boto3
try:
    with open('awscred.txt')as f:
        lines = f.read().splitlines()
except:
    print("Path error")
#Connecting to s3 client
try:
    s3 = boto3.client(
        's3',
        aws_access_key_id=lines[0],
        aws_secret_access_key=lines[1],
    )
except:
    print("connection error")

#Creating a s3 bucket
try:
    s3.create_bucket(
        Bucket='phani06062020',
        CreateBucketConfiguration= {'LocationConstraint': 'ap-south-1'}
    )
except:
    print("Bucket was not created")
#To see the list of buckets
response = s3.list_buckets()

for bucket in response['Buckets']:
    print(bucket)
#Uploading a csv data file to s3 bucket
s3.upload_file("HistoricalQuotes.csv",'phani06062020',"stockData1.csv")

#Reading the data from s3 bucket
import pandas as pd
data = pd.read_csv("s3://phani06062020/stockData1.csv")

data.head()
