### Network Security Project For Phisiing Data

 we need to create a machinelearning model wheather the website is fake or legit

ETL - Extract - Transform - Load

Mongo DB - Source - local dataset readiing the csv file (Data might come from nay other sources like API, S3 Bucket
Sources, SQL)
           Transformation - Basic pre processing and cleaning the raw data and convert into Json
           Destination - Save the in destination - Mongo DB


What is Records:

lest say 
A b c columns
1 2 2

will be converted json {a:1, b:2,c:3}
It should be always key value format  -->  records convert key vaule pair



Data Ingestion:

Read the data from mongo DB 
What is Data ingestion Config?
Data ingestion store
Train and test split and Validation
drop unwanted columns
Directory
 All these output is Data ingestion Artifact ( in the feature store - csv .Raw)
 Then Ingested folder - Train and test






Data Validation

Data Validation - Same Schema means no of column, features and distribution should also be same.
Data drift - Checking the distribution of data means When we are training the data 's distribution and new data distribution shoud be same.
Validate the no of columns Numerical column exist or not.





