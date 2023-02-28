import json
import os, sys
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

    message = json.loads(event['Records'][0]['Sns']['Message'])

    raw_df_key = message['Records'][0]['s3']['object']['key']
    raw_df = pd.read_csv(s3_resource.Object(bucket_name='my-bucket',
                                            key=raw_df_key)
                                            .get()['Body']) \
                                            .fillna(0)
                                            
    with my_raw_table.batch_writer(overwrite_by_pkeys=['departure_id', 'return_id']) as batch_writer:
        for _, row in raw_df.iterrows():
            batch_writer.put_item(Item={'departure': row['departure'],
                                        'return': row['return'],
                                        'departure_id': int(row['departure_id']),
                                        'departure_name': row['departure_name'],
                                        'return_id': int(row['return_id']),
                                        'return_name': row['return_name'],
                                        'distance (m)': int(row['distance (m)']),
                                        'duration (sec.)': int(row['duration (sec.)']),
                                        'avg_speed (km/h)': Decimal(str(row['avg_speed (km/h)'])),
                                        'departure_latitude': Decimal(str(row['departure_latitude'])),
                                        'departure_longitude': Decimal(str(row['departure_longitude'])),
                                        'return_latitude': Decimal(str(row['return_latitude'])),
                                        'return_longitude': Decimal(str(row['return_longitude'])),
                                        'Air temperature (degC)': Decimal(str(row['Air temperature (degC)']))})

