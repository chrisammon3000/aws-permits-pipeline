import logging
import csv
import time
import requests
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

#s3 = boto3.resource('s3')
#bucket = s3.Bucket(BUCKET_NAME)

def download_csv(url, file_path):
    try:
        response = requests.get(url)
    except Exception as e:
        logger.info(f"Error retrieving url: {e}")
    try:
        with open(file_path, 'wb') as f:
            f.write(response.content)
            logger.info(f"File created: {file_path}")
    except Exception as e:
        logger.info(f"Error writing CSV: {e}")

    return


def fetch_data(event, context):

    #url = "https://data.lacity.org/api/views/yv23-pmwf/rows.csv"

    url = "https://query.data.world/s/3jh2lg45et7dhrpolk4in4ye24mnaj"
    timestamp = int(time.time())
    file = f'{timestamp}-permits.csv'


    key = f'raw/{file}'
    file_path = f'./tmp/{file}'

    download_csv(url, file_path)
        
    return {
        "message": "Success"
    }

fetch_data('', '')