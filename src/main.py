from src.mqtt import MQTT
from paho.mqtt.client import Client


def main():
    client = Client()
    mqtt = MQTT(client)
    mqtt.run()


if __name__ == '__main__':
    main()
