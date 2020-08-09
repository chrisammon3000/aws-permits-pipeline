import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']
S3_KEY = os.environ['S3_KEY']

s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET)

def transform_raw_data(event, context):

        
    return {
        "message": "SUCCESS"
    }
