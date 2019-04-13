from mock import MagicMock, patch
from unittest import TestCase
from paho.mqtt.client import Client
from src.mqtt import MQTT

import pytest


class TestMQTT(TestCase):
    """Test class to test the mqtt logic, will not test the framework, but rather that
    the code behave as expected
    """

    @patch('os.path.isdir')
    def test_run_path_exception(self, isdir_mock):
        isdir_mock.return_value = False
        client_mock = Client(MagicMock())
        mqtt_client = MQTT(client_mock)

        with pytest.raises(Exception):
            mqtt_client.run()

    @patch('os.path.isdir')
    def test_run_exception(self, isdir_mock):
        isdir_mock.return_value = True
        client_mock = Client(MagicMock())
        client_mock.connect = MagicMock(side_effect=Exception)
        mqtt_client = MQTT(client_mock)

        with pytest.raises(Exception):
            mqtt_client.run()

        self.assertEqual(client_mock.connect.call_count, 1)

    @patch('os.path.isdir')
    def test_run_sucess(self, isdir_mock):
        input = [0, 0, 1]
        isdir_mock.return_value = True
        loop_mock = MagicMock(side_effect=input)

        client_mock = Client(MagicMock())
        client_mock.connect = MagicMock()
        client_mock.loop = loop_mock
        mqtt_client = MQTT(client_mock)
        mqtt_client.run()

        self.assertEqual(client_mock.connect.call_count, 1)
        self.assertEqual(client_mock.loop.call_count, len(input))
