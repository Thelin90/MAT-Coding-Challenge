from src.suscribe import read_suscribed_topics

from src.helper import \
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
        mqtt_client.subscribe(DEFAULT_SUSCRIBE_TOPIC)
        global connected
        connected = True
    else:
        logging.warn('Connection failed')


def on_publish(mqtt_client, userdata, msg):
    """

    :param mqtt_client:
    :param userdata:
    :param msg:
    :return:
    """
    #logging.info('on_publish')


def on_message(mqtt_client, userdata, msg):
    """Callback function for on_message, msg contains
    carCoordinates, it will make sure there are an
    file containing the data for each car.

    :param mqtt_client: mqtt client
    :param userdata:
    :param msg: the message containing the data
    :return:
    """
    #logging.info('on_message')
    write_raw_data(msg)


client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish
client.on_message = on_message
client.connect(Broker, DEFAULT_PORT, TIME_ALIVE)
client.loop_start()

connected = False

while connected is False:
    time.sleep(0.01)

try:
    while True:
        read_suscribed_topics(client)

except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
