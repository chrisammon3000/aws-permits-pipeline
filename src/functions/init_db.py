import logging
import json
#from lib.sql_queries import permits_raw_table_create

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def init_db(event, context):

    print("Name is ({})".format(__name__))

    logger.info(event)

    msg = json.loads(event["Records"][0]["Sns"]["Message"])
    topic = event["Records"][0]["Sns"]["TopicArn"]
    subject = event["Records"][0]["Sns"]["Subject"]
    
    print(type(msg))

    for item in [msg, topic, subject]:
        logger.info(item)
    
    if msg["Event Message"] in ['DB instance created']:
        print("Fetch data!!!")

    #print("INIT QUERY:\n", permits_raw_table_create)

    return {
        "message": "SUCCESS"
    }
