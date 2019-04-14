from src.helpers.helper import \
    write_file,\
    extract_gps_data,\
    extract_timestamp,\
    create_carstatus_topic_data,\
    event_car_position_msg, \
    find_distance_meter, \
    find_velocity_mph

from unittest import TestCase
from mock import patch, mock_open
from collections import deque

import json
import pytest


class TestHelper(TestCase):

    def setUp(self):
        self.fake_deque_data_success = deque([
            '{"carIndex":1,'
            '"location":{"lat":12345.00,"long":-1.23456},'
            '"timestamp":123}\n',
            '{"carIndex":1,"location":{"lat":12345.67,"long":-1.234569},'
            '"timestamp":1234}\n'
        ], maxlen=2)

        self.fake_deque_data_failure = deque([
            '{"carIndex":1,'
            '"location":{"":12345.00,"long":-1.23456},'
            '"":123}\n',
            '{"carIndex":1,"location":{"lat":12345.67,"long":-1.234569},'
            '"":1234}\n'
        ], maxlen=2)

    def test_write_file_sucess(self):
        mocked_open = mock_open(read_data='fakepath/fakefile')
        with patch('builtins.open', mocked_open, create=True) as mock_file:
            write_file(
                'fakefile',
                'fakedata1, fakedata2',
                'fakepath'
            )
            self.assertEqual(mock_file.call_count, 1)

    def test_write_file_datatype_failure(self):
        mocked_open = mock_open(read_data=Exception)
        with patch('builtins.open', mocked_open, create=True) as mock_file:
            with pytest.raises(ValueError, match='data is not str format'):
                write_file(
                    'fakefile',
                    b'fakedata',
                    'fakepath'
                )
                self.assertEqual(mock_file.call_count, 1)

    def test_extract_gps_data_success(self):
        data = extract_gps_data(self.fake_deque_data_success)
        expected_res = ((12345.00, -1.23456), (12345.67, -1.234569))
        self.assertEqual(data, expected_res)

    def test_extract_timestamp_success(self):
        data = extract_timestamp(self.fake_deque_data_success)
        expected_res = (123, 1234)
        self.assertEqual(data, expected_res)

    def test_create_carstatus_topic_data(self):
        carstatus = create_carstatus_topic_data(1234.0, 1, 'SPEED', 123)
        expected_res = json.dumps(
            {
                "timestamp": 1234.0,
                "carIndex": 1,
                "type": "SPEED",
                "value": 123
             }
        ) + '\n'

        self.assertEqual(carstatus, expected_res)

    def test_event_car_position_msg_success(self):
        expected_res0 = 'car 2 goes 1 steps behind =`('
        expected_res1 = ''
        row1 = {
            'timestamp': 1234.0,
            'carIndex': 1,
            'type': 'POSITION',
            'value': 1
        }
        pos0 = 1
        pos1 = 2

        carpos0 = event_car_position_msg(row1, pos0, pos1)

        pos1 = 1

        carpos1 = event_car_position_msg(row1, pos0, pos1)

        self.assertEqual(carpos0, expected_res0)
        self.assertEqual(carpos1, expected_res1)

    def test_find_distance_meter_success(self):
        expected_res0 = 74500.70375694927
        distance = find_distance_meter((12345.00, -1.23456), (12345.67, -1.234569))
        self.assertEqual(distance, expected_res0)

    def test_find_velocity_success(self):
        expected_res0 = 80.31
        speed = find_velocity_mph(7.180676290826536, 1555273750551.0, 1555273750751.0)
        self.assertEqual(speed, expected_res0)

    def test_extract_gps_data_failure(self):
        with pytest.raises(ValueError, match='invalid gps data'):
            extract_gps_data(self.fake_deque_data_failure)

    def test_extract_timestamp_failure(self):
        with pytest.raises(ValueError, match='invalid timestamp data'):
            extract_timestamp(self.fake_deque_data_failure)

    def test_create_carstatus_topic_data_failure(self):
        with pytest.raises(ValueError, match='invalid data'):
            create_carstatus_topic_data(None, None, None, None)

    def test_find_distance_meter_failure(self):
        with pytest.raises(ValueError, match='tuple or tuples are None'):
            find_distance_meter(None, None)

        with pytest.raises(ValueError, match='gps data need to be a tuple per lat and long'):
            find_distance_meter(0, 1)

    def test_find_velocity_mph_failure(self):
        with pytest.raises(ValueError, match='input arguments must be float'):
            find_velocity_mph(None, None, None)

        with pytest.raises(ZeroDivisionError):
            find_velocity_mph(0.0, 1555269104.0, 1555269104.0)














