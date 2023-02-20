from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.dates import days_ago


AWS_S3_CONN_ID = "aws_default"

def s3_load():
    s3_hook = S3Hook()
    s3_hook.load_file(filename='dags/data/data_2016-05.csv',
                        key='data_2016-05.csv',
                        bucket_name='my-bucket') #key='test',

default_args = {
    'owner':'airflow',
    'start_date': days_ago(3) 
}

with DAG(
    dag_id="aws_test_upload",
    default_args=default_args,
    description='Data pipeline dag',
    schedule_interval=None,
    start_date=datetime.now(),
    catchup=False,
) as dag:

    t1 = PythonOperator(
        task_id="s3_load_task",
        python_callable=s3_load)

    t1