from src.helpers.helper import DATA_CARSTATUS_PATH, TS_INDEX, find_car_position
from src.publish_topics import publish_carstatus_topic, publish_events_topic
from ftfy import fix_text
from collections import deque

import json
import glob


def read_suscribed_topics(client):
    """Function will read the data from the subscribed raw carStatus topic written to <car>_carCoordinates.txt,
    will send them to be published. Push them to the topic.

    :param client:
    :return:
    """
    for filename in glob.iglob(DATA_CARSTATUS_PATH + '**/*', recursive=True):
        with open(filename, 'r') as file:
            try:
                rows = deque(file, 2)

                if len(rows) == 2:
                    row0, row1 = rows[0], rows[1]

                    if isinstance(row0, str):
                        row0 = fix_text(row0)
                        data0, data1 = json.loads(row0), json.loads(row1)

                    else:
                        data0, data1 = json.loads(row0.decode('utf-8')), json.loads(row1.decode('utf-8'))

                    if data1['type'] == 'SPEED':
                        publish_carstatus_topic(data1, 'SPEED', client)

                    elif data1['type'] == 'POSITION':
                        ts = data1.get(TS_INDEX)
                        pos0, pos1 = data0.get('value'), data1.get('value')
                        publish_carstatus_topic(data1, 'POSITION', client)
                        msg = find_car_position(data1, pos0, pos1)
                        publish_events_topic(msg, ts, client)

            except ValueError as e:
                raise e
