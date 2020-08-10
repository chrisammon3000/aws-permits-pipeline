import os
import logging
import boto3
import json
from events.s3_trigger import s3_trigger

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']
#S3_RAW_FOLDER = os.environ['S3_RAW_FOLDER']

s3 = boto3.client('s3')


def transform_raw_data(event, context):

    logger.info(f"Event: {event}")

    for record in event['Records']:
        key = record['s3']['object']['key']
        logger.info(f"Key: {key}")
        response = s3.get_object(Bucket=S3_BUCKET, Key=key)
        logger.info(f"Response: {response}")
        content = response['Body']
        jsonObject = json.loads(content.read())
        logger.info(f"Content: {jsonObject[:100]}")


    # # Convert to for loop
    # for record in event['Records']:

    #     key = record['s3']['object']['key']

    #     logger.info("Key:\n", key)

        #response = s3.get_object(Bucket=S3_BUCKET, Key=key)

        #logger.info("Response:\n", response)

    # content = response['Body']

    # jsonObject = json.loads(content.read)
        
    return {
        "message": "SUCCESS"
    }
