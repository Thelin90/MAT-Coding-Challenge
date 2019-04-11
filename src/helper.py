from collections import deque, Counter
from haversine import haversine

import json
import datetime as dt
import os

DEFAULT_SUSCRIBE_TOPIC = 'carCoordinates'
POS = 'POSITION'
SPEED = 'SPEED'
TS_INDEX = 'timestamp'
CAR_INDEX = 'carIndex'
LOCATION_INDEX = 'location'
DATA_PATH = os.getcwd() + '/data/raw_data/'
DATA_CARSTATUS_PATH = os.getcwd() + '/data/topic_carstatus/'
DATA_EVENTS_PATH = os.getcwd() + '/data/topic_events/'
Broker = '127.0.0.1'
DEFAULT_PORT = 1883
TIME_ALIVE = 60

car_long_lat_data = []


def transform_topic_data(car):
    """Function to retrieve information to create carstatus topic, will
    write data to file

    :param car:
    :return:
    """
    topic_filename = str(car) + '_' + DEFAULT_SUSCRIBE_TOPIC + '.txt'

    with open(os.path.join(DATA_PATH, topic_filename), "r") as raw_data_file:
        raw_data_carstatus = deque(raw_data_file, maxlen=2)

        d0 = json.loads(raw_data_carstatus[0]).get(LOCATION_INDEX)
        d1 = json.loads(raw_data_carstatus[1]).get(LOCATION_INDEX)
        st0, st1 = (d0.get('lat'), d0.get('long')), (d1.get('lat'), d1.get('long'))

        t0 = float(json.loads(raw_data_carstatus[0]).get(TS_INDEX))
        t1 = float(json.loads(raw_data_carstatus[1]).get(TS_INDEX))

        if len(car_long_lat_data) == 6:
            car_long_lat_data[car] = [st1]
            car_positions = find_positions()

            topic_carstatus_position = 'carStatus_positions.txt'
            topic_events = 'events.txt'

            write_topic(
                topic_carstatus_position,
                create_carstatus_topic_data(t1, car, POS, car_positions[car][1] + 1),
                DATA_CARSTATUS_PATH
            )

            compare = lambda x, y: Counter(x) == Counter(y)

            print('latest: ', car_positions)
            #if tmp.sort() == car_positions.sort():
                #print("yes")
            #write_event_file(topic_events, t1, str(car_positions[0][1]) + ' ' + str(car))

        else:
            car_long_lat_data.append([st1])
          #  tmp.append(st1)

        distance = find_distance_meter(st0, st1)
        curr_speed = find_velocity_mph(distance, t0, t1)
        topic_carstatus_speed = str(car) + '_carStatus_speed.txt'

        write_topic(
            topic_carstatus_speed,
            create_carstatus_topic_data(t1, car, SPEED, curr_speed),
            DATA_CARSTATUS_PATH
        )


def create_events_topic_data(ts, msg):
    return json.dumps(
        {
            'timestamp': ts,
            'text': msg,
        }
    ) + '\n'


def create_carstatus_topic_data(ts, car, actual_type, value):
    return json.dumps(
        {
            # t1 because this is the current ts the car is in
            "timestamp": ts,
            "carIndex": car,
            "type": actual_type,
            "value": value
        }
    ) + '\n'


def write_raw_data(msg):
    if msg.topic == DEFAULT_SUSCRIBE_TOPIC:
        car = json.loads(
            msg.payload.decode()
        )[CAR_INDEX]

        raw_data = str(car) + '_' + DEFAULT_SUSCRIBE_TOPIC + '.txt'

        # in a real application this would have been perhaps an S3 bucket writing
        # instead! (Minio locally) but let's keep it simple!
        with open(os.path.join(DATA_PATH, raw_data), 'a') as raw_data_file:
            raw_data_file.writelines(msg.payload.decode() + '\n')

        transform_topic_data(car)


def write_topic(file, data, path):
    """

    :param file:
    :param data:
    :param path:
    :return:
    """
    # running out of time so just sending events
    with open(os.path.join(path, file), 'a') as topic:
        topic.writelines(data)


def find_positions():
    """Function to get the position of the cars, not sure if this actually works properly,
    I had an idea where I would be able to check which cars distance value that get closer to eachother
    to be able to detect when a car drives past another car, but I am not sure how that would be implemented.
    I keep this for now.

    :return: list with tuples containing position of car with the dist value in comparison
    """
    global sorted_leading_board

    tmp = [0, 0, 0, 0, 0, 0]
    for i in range(len(tmp)):
        d0 = car_long_lat_data[i][0]
        for j in range(len(tmp)):
            if i != j:
                d1 = car_long_lat_data[j][0]
                tmp[j] = haversine(d0, d1) * 1000

        sorted_leading_board = sorted(((v, i) for i, v in enumerate(tmp)), reverse=False)

    return sorted_leading_board


def find_distance_meter(dist0, dist1):
    """Function calculates distance in meter between long, lat for each car
    :param dist0:
    :param dist1:
    :return: the calculated distance in meters between the long, lat points
    """
    distance = haversine(dist0, dist1) * 1000
    return distance


def find_velocity_mph(distance, t0, t1):
    """Function calculates the speed in mph for each car
    :param distance:
    :param t0:
    :param t1:
    :return:
    """
    t0 = t0 / 1000.0
    t1 = t1 / 1000.0

    ts0 = dt.datetime.fromtimestamp(t0).strftime('%Y-%m-%d %H:%M:%S.%f')
    ts1 = dt.datetime.fromtimestamp(t1).strftime('%Y-%m-%d %H:%M:%S.%f')
    ts0 = dt.datetime.strptime(ts0, "%Y-%m-%d %H:%M:%S.%f")
    ts1 = dt.datetime.strptime(ts1, "%Y-%m-%d %H:%M:%S.%f")
    duration = ts1 - ts0
    duration_in_s = duration.total_seconds()

    # this works at least
    return round((distance / duration_in_s) * 2.23693629, 2)

