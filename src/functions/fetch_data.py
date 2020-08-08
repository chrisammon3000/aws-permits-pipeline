import csv
import time
import requests
import boto3

def download_csv(url, file_path):
    with requests.get(url, stream=True) as response:
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

def fetch_data(event, context):

    url = "https://data.lacity.org/api/views/yv23-pmwf/rows.csv"

    timestamp = int(time.time())
    file = f'{timestamp}-permits.csv'

    #s3 = boto3.resource('s3')
    #bucket = s3.Bucket(BUCKET_NAME)
    key = f'raw/{file}'

    lambda_path = f'./tmp/{file}'

    r = requests.get(url)

    download_csv(url, lambda_path)

    return {
        "message": "Success"
    }

fetch_data('', '')