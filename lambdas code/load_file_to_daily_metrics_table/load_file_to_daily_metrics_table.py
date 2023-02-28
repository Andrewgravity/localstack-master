import json
import os
from decimal import Decimal
import logging

import boto3
import pandas as pd

endpoint_url = os.getenv('ENDPOINT_URL')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')

def lambda_handler(event, context):
    s3_resource = boto3.resource('s3',
                                 endpoint_url=endpoint_url,
                                 aws_access_key_id=aws_access_key_id,
                                 aws_secret_access_key=aws_secret_access_key,
                                 region_name=region_name)
    dynamodb_resource = boto3.resource('dynamodb',
                                       endpoint_url=endpoint_url,
                                       aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key,
                                       region_name=region_name)

    my_metrics_table = dynamodb_resource.Table('my_daily_metrics_table')

    message = event['Records'][0]['Sns']['Message']
    my_metrics_table_key = json.loads(message)['Records'][0]['s3']['object']['key']

    metrics_df = pd.read_csv(s3_resource.Object(bucket_name='my-bucket',
                                key=my_metrics_table_key) 
                                .get()['Body'],
                                parse_dates=['departure']) \
                                .fillna(0)
                                
    for group_name, group in metrics_df.groupby(pd.Grouper(key='departure', freq='D')):
        if not group.empty:
            with my_metrics_table.batch_writer(overwrite_by_pkeys=['date']) as batch_writer:
                batch_writer.put_item(
                    Item={'date': f'{group_name:%Y-%m-%d}',
                          'avg_distance_m': Decimal(str(metrics_df['distance (m)'].mean())),
                          'avg_duration_sec': Decimal(str(metrics_df['duration (sec.)'].mean())),
                          'avg_speed_km_h': Decimal(str(metrics_df['avg_speed (km/h)'].mean())),
                          'avg_air_temperature_c': Decimal(str(metrics_df['Air temperature (degC)'].mean()))})
