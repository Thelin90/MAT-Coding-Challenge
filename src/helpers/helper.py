from haversine import haversine

import json
import datetime as dt
import os

DEFAULT_SUBSCRIBED_TOPIC = 'carCoordinates'
POS = 'POSITION'
SPEED = 'SPEED'
TS_INDEX = 'timestamp'
CAR_INDEX = 'carIndex'
LOCATION_INDEX = 'location'
DATA_PATH = os.getcwd() + '/data/raw_data/'
DATA_CARSTATUS_PATH = os.getcwd() + '/data/topic_carstatus/'
TOPIC_CARSTATUS_POSITION = 'carStatus_positions.txt'
Broker = '127.0.0.1'
INDEX_LIMIT = 6
DEFAULT_PORT = 1883
TIME_ALIVE = 60
MPH_CONST = 2.23693629
M_CONST = 1000


def write_file(file, data, path):
    """Function to write data to file for each car from subscribed topic
    in regards to position and speed
    :param file:
    :param data:
    :param path:
    :return:
    """
    path = os.path.join(path, file)

    if isinstance(data, str):
        with open(path, 'a') as topic:
            topic.writelines(data)
    else:
        raise ValueError('data is not str format')


def extract_gps_data(data):
    """Function to extract gps data
    :param data: data containing gps data
    :return: tuple of the latest two lat, long tuple pairs
    """
    d0 = json.loads(data[0]).get(LOCATION_INDEX)
    d1 = json.loads(data[1]).get(LOCATION_INDEX)

    if d0.get('lat') is None or d0.get('long') is None or d1.get('lat') is None or d1.get('long') is None:
        raise ValueError('invalid gps data')
    else:
        st0, st1 = (d0.get('lat'), d0.get('long')), (d1.get('lat'), d1.get('long'))
    return st0, st1


def extract_timestamp(data):
    """Function to extract timestamp
    :param data: data containing timestamp
    :return: tuple for the two latest timestamps
    """
    t0 = json.loads(data[0]).get(TS_INDEX)
    t1 = json.loads(data[1]).get(TS_INDEX)

    if t0 is None or t1 is None:
        raise ValueError('invalid timestamp data')
    else:
        return float(t0), float(t1)


def create_carstatus_topic_data(ts, car, actual_type, value):
    """Create event for carstatus topic

    :param ts: unix timestamp
    :param car: car as an integer
    :param actual_type: SPEED | POSITION
    :param value: mph (float) / place (integer)
    :return: carstatus json
    """
    if ts is None or car is None or actual_type is None or value is None:
        raise ValueError('invalid data')

    return json.dumps(
        {
            # t1 because this is the current ts the car is in
            "timestamp": ts,
            "carIndex": car,
            "type": actual_type,
            "value": value
        }
    ) + '\n'


def event_car_position_msg(row, pos0, pos1):
    """

    :param row:
    :param pos0:
    :param pos1:
    :return:
    """
    if pos0 != pos1:
        car = row.get('carIndex') + 1
        ahead = pos0 - pos1
        behind = pos1 - pos0

        return 'car ' f'{car}' ' goes ' f'{ahead}' ' steps ahead =D' if pos0 > pos1 \
            else 'car ' f'{car}' ' goes ' f'{behind} steps behind =`('
    else:
        return ''


def find_positions(car_long_lat_data):
    """Function to get the position of the cars, not sure if this actually works properly,
    I had an idea where I would be able to check which cars distance value that get closer to eachother
    to be able to detect when a car drives past another car, but I am not sure how that would be implemented.
    I keep this for now.

    Note, I will not test this because... I don't really like this solution and it should be fixed so
    leaving it for now

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
    if dist0 is None or dist1 is None:
        raise ValueError('tuple or tuples are None')
    elif not isinstance(dist0, tuple) or not isinstance(dist1, tuple):
        raise ValueError('gps data need to be a tuple per lat and long')
    else:
        distance = haversine(dist0, dist1) * M_CONST
        return distance


def find_velocity_mph(distance, t0, t1):
    """Function calculates the speed in mph for each car
    :param distance:
    :param t0:
    :param t1:
    :return:
    """
    if not isinstance(distance, float) or not isinstance(t0, float) or not isinstance(t1, float):
        raise ValueError('input arguments must be float')

    t0 = t0 / float(M_CONST)
    t1 = t1 / float(M_CONST)

    # extract ts to dateformat
    ts0 = dt.datetime.fromtimestamp(t0).strftime('%Y-%m-%d %H:%M:%S.%f')
    ts1 = dt.datetime.fromtimestamp(t1).strftime('%Y-%m-%d %H:%M:%S.%f')

    # we now have the ms from the ts, let's get delta time
    ts0 = dt.datetime.strptime(ts0, "%Y-%m-%d %H:%M:%S.%f")
    ts1 = dt.datetime.strptime(ts1, "%Y-%m-%d %H:%M:%S.%f")
    delta = ts1 - ts0

    # get duration in seconds
    duration_in_s = delta.total_seconds()

    # calculate m/s * MPH_CONST round 2 decimal = mph
    return round((distance / duration_in_s) * MPH_CONST, 2)

