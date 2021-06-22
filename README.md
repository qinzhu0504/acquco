# Acquco Assignment



## Script dependencies
1. Pandas
2. sqlalchemy
3. Psycopg2


## Current DB Environment
    Postgres Host: shippingdata.ctewbirxs5yo.us-east-2.rds.amazonaws.com

    Port: 1234

    Database: shippingdata

    Schema: shipping

    Table: shippingdata

## S3 and Lambda

    S3 Bucket name: acqucoshippingdata

    Lambda function name: loadShippingData

- Every time there's a new csv file upload to acqucoshippingdata bucket, the lambda function will read the csv, clean the column name, remove NULL and '-' rows, and load to Postgres table shipping.shippingdata with append method.


## analysis.py

#### Potential problems
-  The analysis for cost_per_unit did not account for the SKU number of the item and the unit weight of the item. It could be the most driving factor affecting cost_per_unit
-  The month number is fitted with a linear regression model, and it shows that there's minimal impact from month number value to cost_per_unit, but month number itself doesn't explain holiday shipping.
