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
