from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import pandas as pd

myQuery = "SELECT * FROM co2_emission"

POSTGRES_CONN_ID = 'postgres_conn'

S3_CONN_ID = 's3_conn'

default_args = {
    'owner': 'mulyo',
    'tries': 5,
    'try_delay': timedelta(minutes=2)
}

@dag(
    dag_id = 'postgres_to_s3_dag',
    description = 'ETL postgres to s3',
    default_args = default_args,
    start_date = datetime(2025, 5, 5),
    schedule_interval = '@daily',
    catchup = False,
    tags = ['etl','postgres','s3']
)

def postgres_to_s3():
    
    @task()
    def dataExtraction(query:str, postgres_conn_id:str)->pd.DataFrame:
        hook = PostgresHook(postgres_conn_id)
        conn = hook.get_conn()
        cursor = conn.cursor()

        cursor.execute(query)
        datas = cursor.fetchall()
        datas = [[item[0], float(item[1]), float(item[2]), float(item[3]), float(item[4])] for item in datas]

        cursor.close()
        conn.close()

        columns = ['location','global_total','emission_2023','emission_2000','change_from_2000']

        df = pd.DataFrame(datas, columns=columns)

        return df

    @task()
    def dataTransformation(df:pd.DataFrame):
        # any transformation if needed
        return df

    @task()
    def dataLoading(df:pd.DataFrame, s3_conn_id:str, bucket_name:str):
        s3 = S3Hook(s3_conn_id)
        csv_buffer = df.to_csv(index=False)
        s3_key = 'data/New CO2 Emission.csv'

        s3.load_string(
            csv_buffer,
            key = s3_key,
            bucket_name = bucket_name,
            replace = True
        )

    extracted_df = dataExtraction(myQuery, POSTGRES_CONN_ID)
    transformed_df = dataTransformation(extracted_df)
    dataLoading(transformed_df, S3_CONN_ID, bucket_name="airflow-csv-upload")

etl = postgres_to_s3()

