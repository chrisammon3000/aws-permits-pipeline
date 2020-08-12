import os
import logging
from io import BytesIO, StringIO
import boto3
import numpy as np
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

S3_BUCKET = os.environ['S3_BUCKET']
S3_INT_FOLDER = os.environ['S3_INT_FOLDER']

s3 = boto3.client('s3')

def transform_raw_data(event, context):

    logger.info(f"Event: {event}")

    for record in event['Records']:

        # Read data from S3
        data_key = record['s3']['object']['key']
        logger.info(f'Raw Key: "{data_key}"')

        logger.info(f'Fetching S3 object: "{S3_BUCKET + "/" + data_key}"...')
        data_object = s3.get_object(Bucket=S3_BUCKET, Key=data_key)
        logger.info(f'S3 object fetched: "{S3_BUCKET + "/" + data_key}"')

        data = BytesIO(data_object['Body'].read())
        logger.info(f'Reading into pandas dataframe: "{S3_BUCKET + "/" + data_key}"...')
        data = pd.read_csv(data, encoding='utf8')

        #logger.info(f'Reading CSV: "s3://{S3_BUCKET}/{data_key}"')
        #data = pd.read_csv("s3://" + S3_BUCKET + "/" + data_key)

        # Rename columns
        cols = list(data.columns)
        logger.info(cols)

        data.columns = map(replace_chars, cols)
        logger.info(data.columns)

        # Apply transform
        logger.info(data[["address_start", "street_direction", "street_name", "street_suffix", "suffix_direction",
                      "zip_code"]].head())

        data = create_full_address(data)

        logger.info(data['full_address'].head())

        # Write CSV to S3
        int_key = S3_INT_FOLDER + data_key.split('/')[-1] 
        logger.info(f'Int Key: "{int_key}"')
        csv_buffer = StringIO()
        data.to_csv(csv_buffer, header=True, index=False)
        csv_buffer.seek(0)
        body = csv_buffer.getvalue()
        s3.put_object(Bucket=S3_BUCKET, Body=body, Key=int_key)
        logger.info(f'Successful PUT on S3: "{S3_BUCKET + "/" + int_key}"')

    return {
        "message": "SUCCESS"
    }

# Map of character replacements
replace_map = {' ': '_', '-': '_', '#': 'No', '/': '_', 
               '.': '', '(': '', ')': '', "'": ''}

def replace_chars(text):
    for oldchar, newchar in replace_map.items():
        text = text.replace(oldchar, newchar).lower()
    return text

# Concatenate address columns into full_address column
def create_full_address(data):

    # Truncate suffix_direction to first letter (N, S, E, W)
    data['suffix_direction'] = data['suffix_direction'].str[0].fillna('')

    # Convert zip_code to string
    data['zip_code'] = data['zip_code'].fillna(0).replace(0, '').astype(object)

    # Combine address columns to concatenate
    address_columns = ["address_start", "street_direction", "street_name", "street_suffix", "suffix_direction",
                      "zip_code"]

    # Concatenate address values
    data['full_address'] = data[address_columns].fillna('').astype(str).apply(' '.join, axis=1).str.replace('  ', ' ')

    # Replace empty strings with NaN values
    data[address_columns] = data[address_columns].replace('', np.nan)

    data['zip_code'] = data['zip_code'].astype('Int64')
    
    return data

