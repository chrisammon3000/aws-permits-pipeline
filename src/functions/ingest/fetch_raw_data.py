import os
import logging
import csv
import time
import requests
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']
S3_KEY = os.environ['S3_KEY']
URL = os.environ['PERMITS_URL']
#URL = "https://query.data.world/s/3jh2lg45et7dhrpolk4in4ye24mnaj"

s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET)

def download_csv(url, file_path):
    
    # Make request
    try:
        response = requests.get(url)
    except Exception as e:
        logger.info(f"Error retrieving url: {e}")
    
    # Fetch CSV
    try:
        with open(file_path, 'wb') as f:
            f.write(response.content)
            logger.info(f"File created: {file_path}")
    except Exception as e:
        logger.info(f"Error writing CSV: {e}")

    return


def fetch_raw_data(event, context):

    timestamp = int(time.time())

    file = f'{timestamp}-permits.csv'

    file_path = '/tmp/'+ file

    download_csv(URL, file_path)

    try:
        bucket.upload_file(file_path, S3_KEY + file)
        logger.info(f"File uploaded to bucket: {S3_KEY + file}")
    except Exception as e:
        logger.info(f"Error uploading to S3: {e}")
        
    return {
        "message": "SUCCESS"
    }
