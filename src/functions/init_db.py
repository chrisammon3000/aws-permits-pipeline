import os
import logging
import json
import psycopg2
from libs.sql_queries import permits_raw_table_create, titanic_table_create

DB_ENDPOINT = os.environ['DB_ENDPOINT']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def init_db(event, context):

    logger.info(event)

    try:
        logger.info("Attempting connection...")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, 
                                password=DB_PASSWORD, 
                                host=DB_ENDPOINT)
        cur = conn.cursor()
        logger.info(f'Connected to "{DB_NAME}" at "{DB_ENDPOINT}"')
    except Exception as err:
        logger.error(f'Error: "{err}"')
        return -1

    try:
        logger.info("Executing query...")
        # Alternate with titanic data for testing
        cur.execute(titanic_table_create.format(DB_NAME=DB_NAME,DB_USER=DB_USER))
        # cur.execute(permits_raw_table_create.format(DB_NAME=DB_NAME,DB_USER=DB_USER))
        conn.commit()
        logger.info('Query successful')
        cur.close()
        logger.info(f'Closed connection to "{DB_NAME}" at "{DB_ENDPOINT}')
    except Exception as err:
        logger.error(f'Error: "{err}"')
        cur.close()
        logger.info(f'Closed connection to "{DB_NAME}" at "{DB_ENDPOINT}')
        return -1

    # msg = json.loads(event["Records"][0]["Sns"]["Message"])
    # topic = event["Records"][0]["Sns"]["TopicArn"]
    # subject = event["Records"][0]["Sns"]["Subject"]
    
    # print(type(msg))

    # for item in [msg, topic, subject]:
    #     logger.info(item)
    
    # if msg["Event Message"] in ['DB instance created']:
    #     print("Fetch data!!!")

    #print("INIT QUERY:\n", permits_raw_table_create)

    return 0


if __name__ == "__main__":
    init_db("", "")