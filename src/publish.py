from src.helper import \
    TS_INDEX, \
    CAR_INDEX

import json


def publish_events_topic(msg, client):
    client.publish(
        'events',
        json.dumps({
            'timestamp': msg[TS_INDEX],
            'text': msg['text']
        })
    )


def publish_carstatus_topic(msg, actual_type, client):
    """Function that will publish data to topics

    :param msg: the content that will be written to the topic
    :param actual_type: determine if it is 'SPEED' or 'POSITION'
    """
    client.publish(
        'carStatus',
        json.dumps({
            "timestamp": msg[TS_INDEX],
            "carIndex": msg[CAR_INDEX],
            "type": actual_type,
            "value": msg['value']
        }),
        0
    )
