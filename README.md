# etl_postgres_to_s3
# *Overview*
Project repo to demonstrate automate ETL process with Apache Airflow orchestration. The process start from extracting data from PostgreSQL database, transforming the data using Python with pandas data manipulation, finally load into AWS S3.
# *Prerequisites*
To follow along this project need to be available on your system:
- PostgreSQL running with data ready
  ```bash
  sudo systemctl status postgresql
  ```
- Apache Aiflow running
  ```bash
  airflow webserver --port 8080

  airflow scheduler
  ```
- AWS S3 account
# *Project Flow*
Automate ETL from postgresql to AWS S3:
1. Load necesary libs -- airflow decorators, airflow providers, pandas
   ```python3
   from airflow.decorators import dag, task
   from airflow.providers.postgres.hooks.postgres import PostgresHook
   from airflow.providers.amazon.aws.hooks.s3 import S3Hook
   from datetime import datetime, timedelta
   import pandas as pd
   ```
3. Create connection -- PostgeSQL, AWS S3
   ```python3
   POSTGRES_CONN_ID = 'postgres_conn'

   S3_CONN_ID = 's3_conn'
   ```
5. ETL flow -- data extraction(postgresql) -> data transformation(pandas) -> data loading (s3)
   ```python3
   # data extraction(postgresql)
   extracted_df = dataExtraction(myQuery, POSTGRES_CONN_ID)
   
   # data transformation(pandas)
   transformed_df = dataTransformation(extracted_df)

   # data loading (s3)
   dataLoading(transformed_df, S3_CONN_ID, bucket_name="airflow-csv-upload")
   ```
7. Close connection 
  ```python3
  cursor.close()
  conn.close()
  ```
