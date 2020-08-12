import os
import logging
from io import StringIO
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']

s3 = boto3.client('s3')

def load_raw_data_rds(event, context):

    logger.info(f"Event: {event}")

    for record in event['Records']:

        # Read data from S3
        data_key = record['s3']['object']['key']
        logger.info(f'Raw Key: "{data_key}"')
        

    return {
        "message": "SUCCESS"
    }
