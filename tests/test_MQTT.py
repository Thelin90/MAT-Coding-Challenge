from mock import MagicMock, patch
from unittest import TestCase
from paho.mqtt.client import Client
from src.mqtt import MQTT

import pytest

LOAD_SUBSCRIBED_TOPIC = 'src.mqtt.load_subscribed_topics'


class TestMQTT(TestCase):
    """Test class to test the mqtt logic, will not test the framework, but rather that
    the code behave as expected
    """

    @patch('os.path.isdir')
    @patch(LOAD_SUBSCRIBED_TOPIC)
    def test_run_success(self, load_subscribed_topics_mock, isdir_mock):
        # mock function call to load subscribed topics
        load_subscribed_topics_mock.return_value = MagicMock()
        input = [0, 0, 1]
        isdir_mock.return_value = True
        loop_mock = MagicMock()
        loop_mock.side_effect = input

        client_mock = Client(MagicMock())
        client_mock.connect = MagicMock()
        client_mock.loop = loop_mock
        mqtt_client = MQTT(client_mock)
        mqtt_client.run()

        self.assertEqual(client_mock.connect.call_count, 1)
        self.assertEqual(client_mock.loop.call_count, len(input))

    @patch('os.path.isdir')
    def test_run_path_exception(self, isdir_mock):
        isdir_mock.return_value = False
        client_mock = Client(MagicMock())
        mqtt_client = MQTT(client_mock)

        with pytest.raises(ValueError, match=r'wrong path'):
            mqtt_client.run()

    @patch('os.path.isdir')
    def test_run_exception(self, isdir_mock):
        isdir_mock.return_value = True
        client_mock = Client(MagicMock())
        client_mock.connect = MagicMock(
            side_effect=ConnectionAbortedError('connection aborted')
        )
        mqtt_client = MQTT(client_mock)

        with pytest.raises(ConnectionAbortedError, match=r'connection aborted'):
            mqtt_client.run()

        self.assertEqual(client_mock.connect.call_count, 1)
