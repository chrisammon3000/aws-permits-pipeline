import json


def init_db(event, context):

    # Run initial query on database:
    # - see other examples with postgres (san089)

    return {
        "message": "SUCCESS",
        "event": event
    }
