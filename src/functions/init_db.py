import os
import logging
import json
import psycopg2
#from lib.sql_queries import permits_raw_table_create

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
        cur.execute(permits_raw_table_create.format(DB_NAME=DB_NAME,DB_USER=DB_USER))
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

permits_raw_table_create = ("""
    GRANT ALL PRIVILEGES ON DATABASE "{DB_NAME}" TO {DB_USER};
    CREATE TABLE permits_raw_two (
        "Assessor Book" TEXT,
        "Assessor Page" TEXT,
        "Assessor Parcel" TEXT,
        "Tract" TEXT,
        "Block" TEXT,
        "Lot" TEXT,
        "Reference # (Old Permit #)" TEXT,
        "PCIS Permit #" TEXT,
        "Status" TEXT,
        "Status Date" TEXT,
        "Permit Type" TEXT,
        "Permit Sub-Type" TEXT,
        "Permit Category" TEXT,
        "Project Number" TEXT,
        "Event Code" TEXT,
        "Initiating Office" TEXT,
        "Issue Date" TEXT,
        "Address Start" TEXT,
        "Address Fraction Start" TEXT,
        "Address End" TEXT,
        "Address Fraction End" TEXT,
        "Street Direction" TEXT,
        "Street Name" TEXT,
        "Street Suffix" TEXT,
        "Suffix Direction" TEXT,
        "Unit Range Start" TEXT,
        "Unit Range End" TEXT,
        "Zip Code" TEXT,
        "Work Description" TEXT,
        "Valuation" TEXT,
        "Floor Area-L.A. Zoning Code Definition" TEXT,
        "# of Residential Dwelling Units" TEXT,
        "# of Accessory Dwelling Units" TEXT,
        "# of Stories" TEXT,
        "Contractor's Business Name" TEXT,
        "Contractor Address" TEXT,
        "Contractor City" TEXT,
        "Contractor State" TEXT,
        "License Type" TEXT,
        "License #" TEXT,
        "Principal First Name" TEXT,
        "Principal Middle Name" TEXT,
        "Principal Last Name" TEXT,
        "License Expiration Date" TEXT,
        "Applicant First Name" TEXT,
        "Applicant Last Name" TEXT,
        "Applicant Business Name" TEXT,
        "Applicant Address 1" TEXT,
        "Applicant Address 2" TEXT,
        "Applicant Address 3" TEXT,
        "Zone" TEXT,
        "Occupancy" TEXT,
        "Floor Area-L.A. Building Code Definition" TEXT,
        "Census Tract" TEXT,
        "Council District" TEXT,
        "Latitude/Longitude" TEXT,
        "Applicant Relationship" TEXT,
        "Existing Code" TEXT,
        "Proposed Code" TEXT
    );
    SET statement_timeout = '20s';
""")