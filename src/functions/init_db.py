import os
import logging
import json
import psycopg2
from libs.sql_queries import permits_init_queries, titanic_init_queries

DB_ENDPOINT = os.environ['DB_ENDPOINT']
DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_PORT = os.environ['DB_PORT']

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def init_db(event, context):

    logger.info(event)

    try:
        logger.info("Attempting connection...")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, 
                                password=DB_PASSWORD, 
                                host=DB_ENDPOINT)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        logger.info(f'Connected to "{DB_NAME}" at "{DB_ENDPOINT}"')
    except Exception as err:
        logger.error(f'Error: "{err}"')
        return -1

    try:

        # # permits data
        # # install aws_s3 extension
        # logger.info(f'Executing query: "install aws_s3 extension"')
        # logger.debug(permits_init_queries[0])
        # try:
        #     cur.execute(permits_init_queries[0])
        #     logger.info(f'Query successful')
        # except Exception as err:          
        #     logger.error(f'Unsuccessful query, Error: {err}')

        # # install PostGIS extension
        # logger.info(f'Executing query: "install PostGIS extension"')
        # logger.debug(permits_init_queries[1])
        # try:
        #     cur.execute(permits_init_queries[1])
        #     logger.info(f'Query successful')
        # except Exception as err:
        #     logger.error(f'Unsuccessful query, Error: {err}')

        # # create permits_raw table
        # logger.info(f'Executing query: "CREATE TABLE permits_raw"')
        # logger.debug(permits_init_queries[2].format(DB_NAME=DB_NAME,DB_USER=DB_USER))
        # try:
        #     cur.execute(permits_init_queries[2].format(DB_NAME=DB_NAME,DB_USER=DB_USER))
        #     logger.info(f'Query successful')
        # except Exception as err:
        #     logger.error(f'Unsuccessful query, Error: {err}')

        # titanic data for testing
        # install aws_s3 extension
        logger.info(f'Executing query: "aws_s3 extension"')
        logger.debug(titanic_init_queries[0])
        try:
            cur.execute(titanic_init_queries[0])
            logger.info('Query successful')
            
        except Exception as err:
            logger.error(f'Unsuccessful query, Error: {err}')

        # create titanic_data table
        logger.info(f'Executing query: "CREATE TABLE titanic_data"')
        logger.debug(titanic_init_queries[1].format(DB_NAME=DB_NAME,DB_USER=DB_USER))
        try:
            cur.execute(titanic_init_queries[1].format(DB_NAME=DB_NAME,DB_USER=DB_USER))
            logger.info('Query successful')
        except Exception as err:
            logger.error(f'Unsuccessful query, Error: {err}')

        conn.commit()
        cur.close()

        logger.info(f'Closed connection to "{DB_NAME}" at "{DB_ENDPOINT}')
    except Exception as err:
        logger.error(f'Error: "{err}"')
        cur.close()
        logger.info(f'Closed connection to "{DB_NAME}" at "{DB_ENDPOINT}')
        return -1

    return 0


if __name__ == "__main__":
    init_db("", "")