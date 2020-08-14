import os
import logging
from io import BytesIO
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
        logger.info(f'Data Key: "{data_key}"')

        logger.info(f'Fetching S3 object: "{S3_BUCKET + "/" + data_key}"...')
        data_object = s3.get_object(Bucket=S3_BUCKET, Key=data_key)
        logger.info(f'S3 object fetched: "{S3_BUCKET + "/" + data_key}"')

        data = BytesIO(data_object['Body'].read())
        logger.info(f'Reading into pandas dataframe: "{S3_BUCKET + "/" + data_key}"...')
        data_reader = pd.read_csv(data, encoding='utf8', iterator=True, chunksize=100000)
        data = pd.concat(data_reader, ignore_index=True)

        # Rename columns
        cols = list(data.columns)
        logger.info(cols)
        data.columns = map(replace_chars, cols)
        logger.info("Successfully renamed columns")
        logger.info(list(data.columns))

        # Apply transform
        address_columns = ["address_start", "street_direction", "street_name", "street_suffix", "suffix_direction",
                      "zip_code"]
        logger.info(f'Concatenating columns: {address_columns}...')
        data = create_full_address(data)
        logger.info(data['full_address'].head())
        logger.info(f'New columns:\n{list(data.columns)}')

        col = "Principal Middle Name"
        data.drop(col, inplace=True)
        logger.info(f'Dropped column "{col}"')

        # Save to tmp folder
        file = data_key.split("/")[-1]
        file = '-'.join(file.split("-")[:-1] + ["interim.csv"])
        file_path = '/tmp/'+ file
        logger.info(f'Saving "{file_path}"...')
        data.to_csv(file_path, index=False)
        logger.info(f'Saved "{file_path}".')

        # Upload to S3
        s3_object = S3_INT_FOLDER + file_path.split("/")[-1]
        logger.info(f'Saving S3 object: "{S3_BUCKET + "/" + s3_object}"...')
        s3.upload_file(file_path, S3_BUCKET, s3_object)
        logger.info(f'Saved S3 object: "{S3_BUCKET + "/" + s3_object}"')

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

