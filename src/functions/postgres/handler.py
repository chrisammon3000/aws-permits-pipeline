import json


def hello(event, context):

    # Run initial query on database:
    # - see other examples with postgres (san089)

    return {
        "message": "SUCCESS",
        "event": event
    }