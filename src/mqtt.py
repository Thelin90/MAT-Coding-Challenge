"""
Script to start the suscribe and publish process from mqtt topics
"""
from src.rw_subscribed_topics import write_raw_data, load_suscribed_topics

from src.helpers.helper import \
    DEFAULT_SUBSCRIBED_TOPIC, \
    Broker, \
    DEFAULT_PORT, \
    TIME_ALIVE, \
    DATA_PATH, \
    DATA_CARSTATUS_PATH


import logging
import time
import os

logging.getLogger().setLevel(logging.INFO)


class MQTT(object):

    def __init__(self, client):
        self.client = client

    def run(self):

        if not os.path.isdir(DATA_PATH) or not os.path.isdir(DATA_CARSTATUS_PATH):
            raise Exception

        self.client.connect(Broker, DEFAULT_PORT, TIME_ALIVE)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        try:
            rc = 0
            while rc == 0:
                time.sleep(0.01)
                rc = self.client.loop()

                load_suscribed_topics(self.client)
                time.sleep(0.01)

        except Exception as e:
            logging.warn(e)
            self.client.disconnect()
            self.client.loop_stop()

    def on_connect(self, mqtt_client, userdata, flags, rc):
        """Callback function when connection occur

        :param mqtt_client:
        :param userdata:
        :param flags:
        :param rc:
        """
        logging.info('Connection successful')
        self.client.subscribe(DEFAULT_SUBSCRIBED_TOPIC)

    def on_message(self, mqtt_client, userdata, msg):
        """Callback function for on_message, msg contains
        carCoordinates, it will make sure there are an
        file containing the data for each car.

        :param mqtt_client: mqtt client
        :param userdata:
        :param msg: the message containing the data
        :return:
        """
        write_raw_data(msg)


