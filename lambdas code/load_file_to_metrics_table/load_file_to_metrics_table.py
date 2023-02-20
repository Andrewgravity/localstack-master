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

    my_metrics_table = dynamodb_resource.Table('my_metrics_table')
    message = event['Records'][0]['Body']
    my_metrics_table_key = json.loads(message)['Records'][0]['s3']['object']['key']
    metrics_df = pd.read_csv(s3_resource.Object(bucket_name='my-bucket',
                                key=my_metrics_table_key)  
                                .get()['Body']) \
                                .fillna(0)

    with my_metrics_table.batch_writer(overwrite_by_pkeys=['name']) as batch_writer:
        for _, row in metrics_df.iterrows():
            batch_writer.put_item(Item={'name': row['name'],
                                        'departure_count': int(row['departure_count']),
                                        'return_count': int(row['return_count'])})
