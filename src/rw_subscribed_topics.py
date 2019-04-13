from src.helpers.helper import \
    DATA_CARSTATUS_PATH, \
    DEFAULT_SUBSCRIBED_TOPIC, \
    CAR_INDEX, DATA_PATH, \
    TS_INDEX, \
    find_car_position, \
    transform_topic_data

from src.publish_topics import publish_carstatus_topic, publish_events_topic
from ftfy import fix_text
from collections import deque

import os
import json
import glob


def write_raw_data(msg):
    """Function to write the raw data to file for each car from subscribed topic
    carCoordinates

    :param msg:
    :return:
    """
    if msg.topic == DEFAULT_SUBSCRIBED_TOPIC:
        car = json.loads(
            msg.payload.decode()
        )[CAR_INDEX]

        raw_data = f'{car}' + '_' + DEFAULT_SUBSCRIBED_TOPIC + '.txt'

        # in a real application this would have been perhaps an S3 bucket writing
        # instead! (Minio locally) but let's keep it simple!
        path = os.path.join(DATA_PATH, raw_data)
        try:
            with open(path, 'a') as raw_data_file:
                raw_data_file.writelines(msg.payload.decode() + '\n')

            transform_topic_data(car)
        except Exception as e:
            raise e
    else:
        raise Exception


def load_suscribed_topics(client):
    """Function will read the data from the subscribed raw carStatus topic written to each car,
    sends them to be published.

    :param client:
    :return:
    """
    # create generator object files containing all files in
    # current folder
    files = glob.iglob(DATA_CARSTATUS_PATH + '**/*', recursive=True)

    for filename in files:
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

                        file.close()

            except Exception as e:
                raise e
