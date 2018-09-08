import csv
import boto3
import os

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        downloadPath = '/tmp/file.csv'

        # download object from source bucket and store it in /tmp/
        s3.meta.client.download_file(bucket, key, downloadPath)
        last_2_weightedAverage = []
        with open("/tmp/file.csv", "r") as f:
            reader = csv.DictReader(f)
            for row in list(reader)[-2:]:
                last_2_weightedAverage.append(row['weightedAverage'])
        
        percentage_changed = abs(float(last_2_weightedAverage[1]) - float(last_2_weightedAverage[0])) / float(last_2_weightedAverage[1]) * 100
        
        if percentage_changed > 0.5:
            continue
            # publish to sns notification
        
