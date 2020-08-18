import logging
import json
from postgres.sql_queries import permits_raw_table_create

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def init_db(event, context):

    logger.info(event)

    msg = json.loads(event["Records"][0]["Sns"]["Message"])

    logger.info(msg)

    print("INIT QUERY:\n", permits_raw_table_create)

    return {
        "message": "SUCCESS"
    }
