from airflow import DAG
from airflow.decorators import task
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from smart_file_sensor import SmartFileSensor
import os
from datetime import timedelta
from airflow.utils.dates import days_ago
from datetime import datetime
import sys
import pandas as pd
import csv
from json import dumps
import logging
import configparser
import boto3
from airflow.models.connection import Connection
from airflow.exceptions import AirflowFailException
import json
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

config = configparser.ConfigParser()
config.read('/opt/airflow/airflow.cfg')
dag_path = config['core']['dags_folder']

AWS_REGION= 'us-east-1'
AWS_PROFILE='localstack'
ENDPOINT_URL='http://localhost:4566/'

all_raw_files = os.listdir(f'{dag_path}/data')
all_metrics_files = os.listdir(f'{dag_path}/spark_job')
raw_files = list(filter(lambda f: f.endswith('.csv'), all_raw_files))
metrics_files = list(filter(lambda f: f.endswith('.csv'), all_metrics_files))

def upload_raw_files():
    s3_hook = S3Hook()
    for file in raw_files:
        response = s3_hook.load_file(filename=f'{dag_path}/data/{file}',
                                    key=f'{file}',
                                    bucket_name='my-bucket')

def upload_metrics_files():
    s3_hook = S3Hook()
    for file in metrics_files:
        response = s3_hook.load_file(filename=f'{dag_path}/spark_job/{file}',
                                    key=f'{file}',
                                    bucket_name='my-bucket') 

default_args = {
    'owner':'airflow',
    'start_date': days_ago(3) 
}

dag = DAG(  
    dag_id="upload_all_t0_s3",
    default_args=default_args,
    description='Data pipeline dag',
    schedule_interval=None,
    start_date=datetime.now(),
    catchup=False,
)

upload_metrics_files_to_s3 = PythonOperator(
    task_id='upload-metrics-to-s3',
    python_callable=upload_metrics_files,
    dag=dag
)

upload_raw_files_to_s3 = PythonOperator(
    task_id='upload-raw-files-to-s3',
    python_callable=upload_raw_files,
    dag=dag
)


[upload_raw_files_to_s3, upload_metrics_files_to_s3]
# sensor >> clean >> upload >> notify