"""
Script to start the suscribe and publish process from mqtt topics
"""
from src.read_subscribed_topics import read_suscribed_topics

from src.helpers.helper import \
    write_raw_data, \
    DEFAULT_SUSCRIBE_TOPIC, \
    Broker, \
    DEFAULT_PORT, \
    TIME_ALIVE


import paho.mqtt.client as mqtt
import logging
import time

logging.getLogger().setLevel(logging.INFO)


def on_connect(mqtt_client, userdata, flags, rc):
    """Callback function when connection occur

    :param mqtt_client:
    :param userdata:
    :param flags:
    :param rc:
    """

    if rc == 0:
        logging.info('Connection successful')
        mqtt_client.subscribe(DEFAULT_SUSCRIBE_TOPIC)
        global connected
        connected = True
    else:
        logging.warn('Connection failed')


def on_message(mqtt_client, userdata, msg):
    """Callback function for on_message, msg contains
    carCoordinates, it will make sure there are an
    file containing the data for each car.

    :param mqtt_client: mqtt client
    :param userdata:
    :param msg: the message containing the data
    :return:
    """
    if not mqtt_client == client:
        logging.warn('on_message failed')
        raise ValueError(mqtt_client)
    else:
        write_raw_data(msg)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(Broker, DEFAULT_PORT, TIME_ALIVE)
client.loop_start()

connected = False

while connected is False:
    time.sleep(0.01)

try:
    while True:
        time.sleep(0.01)
        read_suscribed_topics(client)
        time.sleep(0.01)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
