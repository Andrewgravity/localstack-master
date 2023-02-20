import json
import os
from decimal import Decimal
import logging

import boto3
import pandas as pd

def lambda_handler(event, context):
    s3_resource = boto3.resource('s3',
                                 endpoint_url='http://localhost:4566',
                                 aws_access_key_id='test',
                                 aws_secret_access_key='test',
                                 region_name='us-east-1')
    dynamodb_resource = boto3.resource('dynamodb',
                                       endpoint_url='http://localhost:4566',
                                       aws_access_key_id='test',
                                       aws_secret_access_key='test',
                                       region_name='us-east-1')

    my_metrics_table = dynamodb_resource.Table('my_monthly_metrics_table')
    message = event['Records'][0]['Sns']['Message']
    my_metrics_table_key = json.loads(message)['Records'][0]['s3']['object']['key']
    metrics_df = pd.read_csv(s3_resource.Object(bucket_name='my-bucket',
                                key=my_metrics_table_key)  
                                .get()['Body'],
                                parse_dates=['departure']) \
                                .fillna(0)
    my_metrics_date = f"{metrics_df['departure'][0]:%Y-%m}-01"
    my_metrics_table.put_item(
        Item={'date': my_metrics_date,
              'avg_distance_m': Decimal(str(metrics_df['distance (m)'].mean())),
              'avg_duration_sec': Decimal(str(metrics_df['duration (sec.)'].mean())),
              'avg_speed_km_h': Decimal(str(metrics_df['avg_speed (km/h)'].mean())),
              'avg_air_temperature_c': Decimal(str(metrics_df['Air temperature (degC)'].mean()))})
