from src.helpers.helper import \
    TS_INDEX, \
    CAR_INDEX

import json


def publish_events_topic(msg, ts, client):
    """Function that will publish data for event topic

    :param msg: message of pos status
    :param ts: timestamp value
    :param client: the mqtt client
    :return:
    """
    if len(msg) > 0:
        client.publish(
            'events',
            json.dumps({
                'timestamp': ts,
                'text': msg
            }),
            0
        )
    else:
        raise ValueError


def publish_carstatus_topic(msg, actual_type, client):
    """Function that will publish data to carstatus topic

    :param msg: the content that will be written to the topic
    :param actual_type: determine if it is 'SPEED' or 'POSITION'
    :param client: the mqtt client
    """
    if len(msg) > 0:
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
    else:
        raise ValueError
