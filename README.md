## StockPricePrediction

This project is about predicting the stock price using live real time data.
In this i used the historical Google stock price data for training and built 
the effective model for predicting Stock prices.I used AWS S3 to store the 
historical data and alphaventageservices for real time Stock  prices. 
The Predicted prices has been projected on the web page using the Flask EC2 instance.

## Software Prerequisites:

- Python3
- Java 8,
- Kafka_2.11-1.0.0,
- Apache-zookeeper-3.5.5,
- pyspark

## Step by step Procedure followed for doing this project:

**Step1**: Creating an AWS account and creating a user and generating the Access key and security key save that file.
Now opening the terminal in ubuntu and install AwsCLI to do that run the following commands
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
**sudo ./aws/install
Now check the aws version using command aws --version
Now we have to configure the aws using command aws configure and write the access key and security key their.

**Step2**: Now we have to open the pycharm and install the necessary modules for our project.
Now create a project folder and creating a one python file for creating bucket in AWS s3 
By using a module boto3 and boto which can be installed by command 
**Pip3 install boto3***
The Bucket name should be unique 
Download a past 5 years Historical data from the following site
https://www.nasdaq.com/market-activity/stocks/goog/historical

Next step is to store this historical data in the bucket which we created in AWS S3.



**Step3**: Now we have to read the data from AWS S3 using python script
So for that we have to import boto3 and read the data using pandas.

While reading the data from S3 please check the time of your vm and actual time 
If there is any difference it may throw a error call permission Forbidden.

After reading the data from S3 Now we have to perform EDA process on data set before training model and applying algorithm.

## Exploratory Data Analysis

**Step4**: Now we have to study the data and make it clean to build a most effective model and we should also decide which are the dependent features and which are independent features.

- In the Eda process we have to check data types of the columns in the dataset in our dataset default is object so we have changed that to float and date to date type.
- I have reindexed the column names
- We have to check for the null values in the columns if any null value is present better to replace it with the average of that column.
- I have checked the correlation of that dataset to know how the variables are correlated with each other and I also checked the descriptive statistics of that dataset.
Now the dataset is ready to train the model 

## Training and testing the model :

**Step5**: Now before training model we have to convert the pandas dataframe to Spark RDD 
For that we have to import SQLcontext and Sparkcontext from pyspark and convert the dataframe to spark RDD

Now we have to import the Linear regression and **vector assembler** from **Pyspark MLLib**
After importing the module we have to use vectorassembler to make all the independent variables to a single column called features.

Now we have to train and test the data by splitting  the data set in ratio in such a way that training should give more data and testing should give less data soo in our case we given
The dataset in ratio 8:2 i.e 80% for training model and 20% for testing data.

Applying the Linear Regression algorithm on the dataset columns features and target variable close and we have to fit the model on train_data 

Now we have to test the model using the test data whether the model is trained correctly or not and after that we have to find the accuracy in our case it is 0.99% 
After that we have to save the model. 

## Alpha Vantage

It is a leading provider of Free API’s for real time and historical data on stocks 
We have to register with this it will generate a key for us and we have to copy that key and save that file in our project directory.

## Kafka installation
Download the **Kafka_2.11-1.0.0 tar** file using wget and untar that.
Download the **Apache-zookeeper-3.5.5** tar file and untar that

Add the following configuration in bashrc or sparkenv.sh
```
export PYSPARK_PYTHON=/usr/bin/python3
export PYSPARK_DRIVER_PYTHON=python3
```
Now go to the spark home directory
``` 
**$ cd Kafka_2.11-1.0.0
       
 **$ ./bin/zookeeper-server-start.sh config/zookeeper.properties “Starting Zookeeper Server”
       
 **$ ./bin/kafka-server-start.sh config/server.properties “Starting Kafka Server”
     
Starting Producer:
 **$ ./bin/kafka-consumer-producer.sh --broker-list localhost:9092 --topic stock_prices
```
Starting consumer
```
 **$ ./bin/kafka-consumer-consumer.sh --bootstrap-service localhost:9092 --topic stock_prices
 ```
- When you enter any message in the producer it has to show in consumer
- Now we have to run the python prods.py in which we have read the live stock data from alpha vantage using keys to the kafka server 
- Now we have to run the cons.py in that we have to read the data from the kafka server and we have to load the model on that data and predict that data.
- Now run the python app.py in which we imported the cons.py to display the result data on the web using Flask and highcharts.

## Deployment

To deploy a flask application, create an EC2 instance with t2 medium and minimum of 15GB of storage with ubuntu OS on AWS.
- Create a http security group to allow the public to view web sites.
- Download the .pem file to access the instance from the local terminal.
- To access instance from local terminal, make ssh connection
```
**ssh -i flask.pem ubuntu@<Elastic IP address of ec2 instance>
```
We can create an Elastic IP so that the ip address may be constant without changing when we start an instance.

Now update packages
```
**sudo apt-get update
```
Install git
```
**sudo apt-get install git
```
Clone the project
```
**Install pip
sudo apt-get install python3-pip
```
Now install required libraries
```
pip3 install -r requirements.txt
 ```
Install Gunicorn3, it is a Python Web Server Gateway Interface HTTP server.
```
**pip3 install gunicorn3
 ```
Configure the gunicorn3 
Open flaskapp
```
**$ cd ls
Run $ gunicorn3 app:app
 
Create Gunicorn as a Service
**Go to /etc/systemd/system/
Cd /etc/systemd/system/
$ sudo vim gunicorn3.service
```
```
**[Unit]
Description=Gunicorn service
After=network.target
[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/Flaskapp
ExecStart=/usr/bin/gunicorn3 --workers 3 --bind unix:flaskapp.sock -m 007 app:app
 ```
 ```
**$ sudo systemctl daemon-reload
$ sudo service gunicorn3 start
$ sudo service gunicorn3 status
 ```
Now Install nginx, Nginx is a web server which can also be used as a reverse proxy, load balancer, mail proxy and HTTP cache.
```
**sudo apt-get install nginx
 ```
Set up the environment as above mentioned procedures such as downloading kafka and running zookeeper and kafka server.
Now going to the kafkahome and run the command to start zookeeper.properties
```
**bin/zookeeper-server-start.sh config/zookeeper.properties
 ```
From kafkahome now run the command to start kafka server 
```
**bin/kafka-server-start.sh config/server.properties
 ```
 
Go to nginx sites-enabled directory
```
**cd /etc/nginx/sites-enabled
 ```
 
create new file
```
**sudo nano flaskapp
 ```
Configure following
```
**server{
    listen 8080;
    server_name <your ec2 instace elastic IP address>;
    
    location / {
          proxy_pass http://127.0.0.1:8000;
    }
}
 ```
Now restart nginx server
```
**sudo service nginx restart
 ```
Now go to the project directory and run the Prod.py in the terminal to read live data from alpha vantage and send it to the kafka server.
We can check the previous jobs by using command 
```
**jobs -l
```
Now run the app command using gunicorn3
```
**gunicorn3 --threads=4 app:app
```
Check the result on web using elasticip followed by 8080 port

## Job Scheduler

- Create job schedule to performane operation autometically.
- The Stock Price Prediction of streaming data's Graph display on webpage with aws instance, have to schedule 4 jobs.
- First running two servers, zookeeper and kafka with a time gap of 5 minutes.
- Running Producer and Visualization code with time gap of 5 minutes.
- Create a crontab for jobs scheduling within 5 minutes.
- create path files in instance to schedule jobs.
- Open Instance in sysytem
- Check "$ crontab -l" for list of running job schedule
- create new jobs then create "crontab -e"
It need Minutes(0-60), Hours(1-24), day of month(1-31), month(1-12), Week(0-6) and job ToDo or location of file Schedule to work
  1. Job schedule to zookeeper 
  ```           
              01 06 * * * cd /home/ubuntu/kafka/nohup bin/zookeeper-server-start.sh config/zookeeper.properties &
                             
          2. Job schedule to kafka
               
              06 06 * * * cd /home/ubuntu/kafka/bin/kafka-server-start.sh config/server.properties

          3. Job schedule to Producer

             11 06 * * * cd python3 /home/ubuntu/StockPricePrediction/Prod.py
          
          4. Job schedule to visulazation

             11 06 * * * cd gunicorn3 --threads=4 /home/ubuntu/StockPricePrediction/app:app

   ## LICENSE
   Phanindra
   licensed under MIT LICENSE
```




