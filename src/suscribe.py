from src.helper import DATA_EVENTS_PATH, DATA_CARSTATUS_PATH, DATA_PATH
from src.publish import publish_events_topic, publish_carstatus_topic
from collections import deque

import json
import glob


def read_suscribed_topics(client):
    """

    :param client:
    :return:
    """
    for filename in glob.iglob(DATA_CARSTATUS_PATH + '**/*', recursive=True):
        with open(filename, 'r') as file:
            data = json.loads(deque(file, 1)[0])

            if data['type'] == 'SPEED':
                publish_carstatus_topic(data, 'SPEED', client)
            elif data['type'] == 'POSITION':
                publish_carstatus_topic(data, 'POSITION', client)

    for filename in glob.iglob(DATA_EVENTS_PATH + '**/*', recursive=True):
        with open(filename, 'r') as file:
            data = json.loads(deque(file, 1)[0])
            # publish_events_topic(data, client)