import os
import logging
import csv
import time
import requests
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']
S3_RAW_FOLDER = os.environ['S3_RAW_FOLDER']
URL = os.environ['PERMITS_URL']
FILENAME = os.environ['FILENAME']
S3_PATH = S3_BUCKET + "/" + S3_RAW_FOLDER

s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET)

def fetch_data(event, context):

    timestamp = int(time.time())
    file = f'{timestamp}-{FILENAME}-raw.csv'
    file_path = '/tmp/'+ file

    try:
        download_csv(URL, file_path)
    except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
        raise SystemExit(err)

    try:
        bucket.upload_file(file_path, S3_RAW_FOLDER + file)
        logger.info(f'File "{file_path}" uploaded as S3 object: "{S3_PATH + file}"')
    except Exception as e:
        logger.info(f"Error uploading to S3: {e}")
        return -1
        
    return 0


def download_csv(url, file_path):
    
    # Make request
    try:
        logger.info(f'Retrieving url: "{URL}"')
        response = requests.get(url)
    except Exception as e:
        logger.info(f'Error retrieving url: {e}')
        return -1
    
    # Fetch CSV
    try:
        with open(file_path, 'wb') as f:
            f.write(response.content)
            logger.info(f'File created: "{file_path}"')
    except Exception as e:
        logger.info(f"Error writing CSV: {e}")
        return -1

    return 0


    if __name__ == "__main__":
        fetch_data("", "")