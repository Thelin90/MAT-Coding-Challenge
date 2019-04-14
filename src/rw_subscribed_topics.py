from src.helpers.helper import \
    DATA_CARSTATUS_PATH, \
    DEFAULT_SUBSCRIBED_TOPIC, \
    CAR_INDEX, DATA_PATH, \
    TS_INDEX, \
    INDEX_LIMIT, \
    POS, \
    SPEED, \
    event_car_position_msg, \
    extract_gps_data, \
    extract_timestamp, \
    find_velocity_mph, \
    find_distance_meter, \
    create_carstatus_topic_data, \
    find_positions, \
    write_file

from src.publish_topics import publish_carstatus_topic, publish_events_topic
from ftfy import fix_text
from collections import deque

import os
import json
import glob

car_long_lat_data = []


def write_raw_data(msg):
    """Function to write the raw data to file for each car from subscribed topic
    carCoordinates

    :param msg: dictionary containing topic info and data
    """

    if msg.topic == DEFAULT_SUBSCRIBED_TOPIC:
        car = json.loads(
            msg.payload.decode()
        )[CAR_INDEX]

        raw_data = f'{car}' + '_' + DEFAULT_SUBSCRIBED_TOPIC + '.txt'

        # in a real application this would have been perhaps an S3 bucket writing
        # instead! (Minio locally) but let's keep it simple!
        path = os.path.join(DATA_PATH, raw_data)

        with open(path, 'a') as raw_data_file:
            raw_data_file.writelines(msg.payload.decode() + '\n')

        transform_topic_data(car)

    else:
        raise ValueError('wrong topic')


def load_subscribed_topics(client, path=DATA_CARSTATUS_PATH):
    """Function will read the data from the subscribed raw carStatus topic written to each car,
    sends them to be published.

    :param client: the mqtt client
    :param path: path for subscribed topic data
    """
    for filename in glob.iglob(path + '**/*', recursive=True):

        with open(filename, 'r') as file:
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
                    msg = event_car_position_msg(data1, pos0, pos1)

                    if len(msg) > 0:
                        publish_events_topic(msg, ts, client)

                    file.close()


def transform_topic_data(car):
    """Function to retrieve information to create carstatus topic, will
    write data to file
    :param car: actual car
    """
    topic_filename = f'{car}' + '_' + DEFAULT_SUBSCRIBED_TOPIC + '.txt'

    with open(os.path.join(DATA_PATH, topic_filename), 'r') as raw_data_file:
        raw_data_carstatus = deque(raw_data_file, maxlen=2)

        st0, st1 = extract_gps_data(raw_data_carstatus)
        t0, t1 = extract_timestamp(raw_data_carstatus)

        if len(car_long_lat_data) == INDEX_LIMIT:
            car_long_lat_data[car] = [st1]
            car_positions = find_positions(car_long_lat_data)

            topic_carstatus_position = f'{car}' + '_carStatus_position.txt'

            # write position
            write_file(
                topic_carstatus_position,
                create_carstatus_topic_data(t1, car, POS, car_positions[car][1] + 1),
                DATA_CARSTATUS_PATH
            )

        else:
            car_long_lat_data.append([st1])

        distance = find_distance_meter(st0, st1)
        curr_speed = find_velocity_mph(distance, t0, t1)
        topic_carstatus_speed = f'{car}' + '_carStatus_speed.txt'

        # write speed
        write_file(
            topic_carstatus_speed,
            create_carstatus_topic_data(t1, car, SPEED, curr_speed),
            DATA_CARSTATUS_PATH
        )
