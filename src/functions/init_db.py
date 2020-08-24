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
logger.setLevel(logging.INFO)

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
        logger.info("Executing queries...")

        # permits data
        # try:
        #     cur.execute(permits_init_queries[0])
        #     logger.info(f'Queries successful: {permits_init_queries[0]}')
        # except Exception as err:
        #     logger.info(f'Error: {err}')
        #     logger.info(f'Unsuccessful query: "{titanic_init_queries[0]}"')

        # try:
        #     cur.execute(permits_init_queries[1])
        #     logger.info(f'Queries successful: {permits_init_queries[1]}')
        # except Exception as err:
        #     logger.info(f'Error: {err}')
        #     logger.info(f'Unsuccessful query: "{titanic_init_queries[0]}"')

        # try:
        #     cur.execute(permits_init_queries[2].format(DB_NAME=DB_NAME,DB_USER=DB_USER))
        #     logger.info(f'Query successful: {permits_init_queries[2].format(DB_NAME=DB_NAME,DB_USER=DB_USER)}')
        # except Exception as err:
        #     logger.info(f'Error: {err}')
        #     logger.info(f'Unsuccessful query: "{titanic_init_queries[0]}"')

        # titanic data for testing
        try:
            cur.execute(titanic_init_queries[0])
            logger.info(f'Query successful: "{titanic_init_queries[0]}"')
        except Exception as err:
            logger.info(f'Error: {err}')
            logger.info(f'Unsuccessful query: "{titanic_init_queries[0]}"')

        try:
            cur.execute(titanic_init_queries[1].format(DB_NAME=DB_NAME,DB_USER=DB_USER))
            logger.info(f'Query successful: "{titanic_init_queries[1].format(DB_NAME=DB_NAME,DB_USER=DB_USER)}"')
        except Exception as err:
            logger.info(f'Error: {err}')
            logger.info(f'Unsuccessful query: "{titanic_init_queries[1].format(DB_NAME=DB_NAME,DB_USER=DB_USER)}"')


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