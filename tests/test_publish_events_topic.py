from unittest import TestCase
from mock import MagicMock
from paho.mqtt.client import Client
from src.mqtt import MQTT
from src.publish_topics import publish_events_topic, publish_carstatus_topic

import pytest


class TestPublish_events_topic(TestCase):

    def setUp(self):
        self.fake_msg = 'fake_msg'
        self.fake_msg_list = {
            'timestamp': 1234.0,
            'carIndex': 3,
            'type': 'fakepos',
            'value': 123
        }
        self.fake_ts = 123434421312.000
        self.fake_type = 'faketype'
        self.client_mock = Client(MagicMock())
        self.mqtt_client = MQTT(self.client_mock)
        self.mqtt_client.connect = MagicMock()
        self.client_mock.publish = MagicMock()

    def test_publish_events_topic_success(self):
        publish_events_topic(
            self.fake_msg,
            self.fake_ts,
            self.client_mock
        )

        self.assertEqual(self.client_mock.publish.call_count, 1)

    def test_publish_carstatus_topic_exception(self):
        with pytest.raises(Exception):
            publish_carstatus_topic('', None, Exception)

    def test_publish_carstatus_topic_success(self):
        publish_carstatus_topic(
            self.fake_msg_list,
            self.fake_type,
            self.client_mock
        )

        self.assertEqual(self.client_mock.publish.call_count, 1)

    def test_publish_events_topic_exception(self):
        with pytest.raises(Exception):
            publish_events_topic('', None, Exception)
