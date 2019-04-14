from unittest import TestCase
from mock import MagicMock, patch
from src.rw_subscribed_topics import write_raw_data, load_subscribed_topics
from src.helpers.helper import DEFAULT_SUBSCRIBED_TOPIC

import io
import pytest

PUBLISH_EVENTS_TOPIC = 'src.rw_subscribed_topics.publish_events_topic'
PUBLISH_CARSTATUS_TOPIC = 'src.rw_subscribed_topics.publish_carstatus_topic'
EVENT_CAR_POS = 'src.rw_subscribed_topics.event_car_position_msg'
TRANSFORM = 'src.rw_subscribed_topics.transform_topic_data'
CREATE_CARSTATUS_TOPIC_DATA = 'src.rw_subscribed_topics.create_carstatus_topic_data'
EXTRACT_GPS_DATA = 'src.rw_subscribed_topics.extract_gps_data'
EXTRACT_TIMESTAMP = 'src.rw_subscribed_topics.extract_timestamp'
FIND_POSITIONS = 'src.rw_subscribed_topics.find_positions'


class TestRWsubscribedTopis(TestCase):

    def setUp(self):
        self.fake_input = b'{"carIndex":1,"location":' \
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

    @patch('os.path.isdir')
    @patch('os.path.join')
    @patch(TRANSFORM)
    def test_write_raw_data_success(self, transform_mock, pathjoin_mock, isdir_mock):
        # mock function call inside function
        isdir_mock.return_value = True
        transform_mock.return_value = MagicMock()
        pathjoin_mock.return_value = self.fake_pathjoin_str
        msg_mock = MagicMock(topic=DEFAULT_SUBSCRIBED_TOPIC, payload=self.fake_input)

        with patch('builtins.open', create=True) as mock_file:
            write_raw_data(msg_mock)
            self.assertEqual(mock_file.call_count, 1)

        # correct logic with transform call
        self.assertEqual(transform_mock.call_count, 1)

    @patch('glob.iglob')
    @patch(PUBLISH_CARSTATUS_TOPIC)
    @patch(PUBLISH_EVENTS_TOPIC)
    @patch(EVENT_CAR_POS)
    def test_load_subscribed_topics_sucess(
            self,
            find_car_pos_mock,
            pub_events_mock,
            pub_carstatus_mock,
            iglob_mock
    ):
        pub_carstatus_mock.return_value = MagicMock()
        pub_events_mock.return_value = MagicMock()
        find_car_pos_mock.return_value = 'fake_msg'

        iglob_mock.return_value = ['fakepath1']

        # correct logic when position
        with patch('builtins.open', side_effect=[self.fake_file_pos], create=True) as mock_file:
            load_subscribed_topics(MagicMock(publish=MagicMock()))
            self.assertEqual(mock_file.call_count, 1)
            self.assertEqual(pub_carstatus_mock.call_count, 1)
            self.assertEqual(pub_events_mock.call_count, 1)
            self.assertEqual(find_car_pos_mock.call_count, 1)

        pub_carstatus_mock.reset_mock()
        pub_events_mock.reset_mock()
        find_car_pos_mock.reset_mock()

        # correct logic when speed
        with patch('builtins.open', side_effect=[self.fake_file_speed], create=True) as mock_file:
            load_subscribed_topics(MagicMock(publish=MagicMock()))
            self.assertEqual(mock_file.call_count, 1)
            self.assertEqual(pub_carstatus_mock.call_count, 1)
            self.assertEqual(pub_events_mock.call_count, 0)
            self.assertEqual(find_car_pos_mock.call_count, 0)

    def test_transform_topic_data_success(self):
        pass

    @patch(TRANSFORM)
    def test_write_raw_data_topic_exception(self, transform_mock):
        # mock function call inside function
        transform_mock.return_value = MagicMock()
        msg_mock = MagicMock(topic='wrong-topic')

        with pytest.raises(ValueError, match=r"wrong topic"):
            write_raw_data(msg_mock)
