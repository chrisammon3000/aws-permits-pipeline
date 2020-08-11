import os
import logging
import boto3
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']
#S3_RAW_FOLDER = os.environ['S3_RAW_FOLDER']

s3 = boto3.client('s3')

def transform_raw_data(event, context):

    logger.info(f"Event: {event}")

    for record in event['Records']:
        key = record['s3']['object']['key']
        logger.info(f"Object Key: {key}")

        dataframe = pd.read_csv("s3://" + S3_BUCKET + "/" + key)
        logger.info(dataframe.head())

        
    return {
        "message": "SUCCESS"
    }
