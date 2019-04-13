from unittest import TestCase
from mock import MagicMock, patch
from src.rw_subscribed_topics import write_raw_data, load_suscribed_topics
from src.helpers.helper import DEFAULT_SUBSCRIBED_TOPIC

import io
import pytest

PUBLISH_EVENTS_TOPIC = 'src.rw_subscribed_topics.publish_events_topic'
PUBLISH_CARSTATUS_TOPIC = 'src.rw_subscribed_topics.publish_carstatus_topic'
FIND_CAR_POS = 'src.rw_subscribed_topics.find_car_position'
TRANSFORM = 'src.rw_subscribed_topics.transform_topic_data'


class TestRWsubscribedTopis(TestCase):

    def setUp(self):
        self.fake_input_exc = '{"carIndex":1,"location":' \
                     '{"lat":52.1245,"long":-1.12345},' \
                     '"timestamp":1234}'

        self.fake_input_corr = b'{"carIndex":1,"location":' \
                               b'{"lat":52.1245,"long":-1.12345},' \
                               b'"timestamp":1234}'

        self.fake_file_pos = io.StringIO(
            '{"timestamp": 123.0, "carIndex": 3, "type": "POSITION", "value": 2}\n'
            '{"timestamp": 123.0, "carIndex": 3, "type": "POSITION", "value": 1}\n'
        )

        self.fake_file_speed = io.StringIO(
            '{"timestamp": 123.0, "carIndex": 3, "type": "SPEED", "value": 2}\n'
            '{"timestamp": 123.0, "carIndex": 3, "type": "SPEED", "value": 1}\n'
        )

        self.fake_pathjoin_str = '/fake_data/fake_raw_data/1_carCoordinates.txt'

    @patch(TRANSFORM)
    @patch('os.path.join')
    def test_write_raw_data_success(self, transform_mock, pathjoin_mock):
        # mock function call inside function
        transform_mock.return_value = MagicMock()
        pathjoin_mock.return_value = self.fake_pathjoin_str
        msg_mock = MagicMock(topic=DEFAULT_SUBSCRIBED_TOPIC, payload=self.fake_input_corr)

        with patch('builtins.open', create=True) as mock_file:
            write_raw_data(msg_mock)
            self.assertEqual(mock_file.call_count, 1)

        # correct logic with transform call
        self.assertEqual(transform_mock.call_count, 1)

    @patch(TRANSFORM)
    def test_write_raw_data_input_exception(self, transform_mock):
        # mock function call inside function
        transform_mock.return_value = MagicMock()
        msg_mock = MagicMock(topic=DEFAULT_SUBSCRIBED_TOPIC, payload=self.fake_input_exc)

        with pytest.raises(Exception):
            write_raw_data(msg_mock)

    def test_write_raw_data_path_exception(self):
        msg_mock = MagicMock(topic='wrong-path')

        with pytest.raises(Exception):
            write_raw_data(msg_mock)

    @patch('glob.iglob')
    @patch(PUBLISH_CARSTATUS_TOPIC)
    @patch(PUBLISH_EVENTS_TOPIC)
    @patch(FIND_CAR_POS)
    def test_load_suscribed_topics_sucess(
            self,
            find_car_pos_mock,
            pub_events_mock,
            pub_carstatus_mock,
            iglob_mock
    ):
        pub_carstatus_mock.return_value = MagicMock()
        pub_events_mock.return_value = MagicMock()
        find_car_pos_mock.return_value = MagicMock()

        iglob_mock.return_value = ['fakepath1']

        # correct logic when position
        with patch('builtins.open', side_effect=[self.fake_file_pos], create=True) as mock_file:
            load_suscribed_topics(MagicMock(publish=MagicMock()))
            self.assertEqual(mock_file.call_count, 1)
            self.assertEqual(pub_carstatus_mock.call_count, 1)
            self.assertEqual(pub_events_mock.call_count, 1)
            self.assertEqual(find_car_pos_mock.call_count, 1)

        pub_carstatus_mock.reset_mock()
        pub_events_mock.reset_mock()
        find_car_pos_mock.reset_mock()

        # correct logic when speed
        with patch('builtins.open', side_effect=[self.fake_file_speed], create=True) as mock_file:
            load_suscribed_topics(MagicMock(publish=MagicMock()))
            self.assertEqual(mock_file.call_count, 1)
            self.assertEqual(pub_carstatus_mock.call_count, 1)
            self.assertEqual(pub_events_mock.call_count, 0)
            self.assertEqual(find_car_pos_mock.call_count, 0)

    @patch('glob.iglob')
    def test_load_suscribed_topics_failure(self, iglob_mock):
        iglob_mock.return_value = [Exception]
        with patch('builtins.open', side_effect=Exception, create=True) as mock_file:
            with pytest.raises(Exception):
                load_suscribed_topics(MagicMock())
                self.assertEqual(mock_file.call_count, 1)
