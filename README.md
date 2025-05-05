# etl_postgres_to_s3
Automate ETL from postgresql to AWS S3:
1. Load necesary libs -- airflow decorators, airflow providers, pandas
2. Create connection -- PostgeSQL, AWS S3
3. ETL flow -- data extraction(postgresql) -> data transformation(pandas) -> data loading (s3)
4. Close connection 
