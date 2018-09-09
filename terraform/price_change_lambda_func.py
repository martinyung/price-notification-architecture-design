import csv
import boto3

s3 = boto3.resource('s3')

def get_lastest_2_price_data(file):
    '''
    - only calculate last 2 weightedAverage because this is near real time notification

    @type  file: string
    @param file: The path to the downloaded csv in lambda temp directory.
    
    @rtype:      list
    @return:     list containing the last 2 weightedAverage
    '''

    lastest_2_weightedAverage = []

    with open('/tmp/file.csv', 'r') as f:
        reader = csv.DictReader(f)

        for row in list(reader)[-2:]:
            lastest_2_weightedAverage.append(float(row['weightedAverage']))

    return lastest_2_weightedAverage

def compute_price_changed(weighted_average1, weighted_average2):
    '''
    - calculate the absolute percentage change between the last 2 weightedAverages

    @type  weighted_average1: float
    @param weighted_average1: the last weightedAverage.
    @type  weighted_average2: float
    @param weighted_average2: the 2nd last weightedAverage.
    
    @rtype:                   float
    @return:                  absolute percentage change between weighted_average1 and weighted_average2
    '''
    return abs(weighted_average1 - weighted_average2) / weighted_average1 * 100

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        download_path = '/tmp/file.csv'
        alert_threshold = 0.5

        # download csv from [Bucket]/crypto/02-data-analysis/USDT_ETH.csv to /tmp/ in lambda
        s3.meta.client.download_file(bucket, key, download_path)

        weighted_average_array = get_lastest_2_price_data(download_path)

        percentage_changed = compute_price_changed(weighted_average_array[1], weighted_average_array[0])
        
        if percentage_changed > alert_threshold:
            continue
            # publish to sns notification
        
