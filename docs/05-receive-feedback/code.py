# Aufgabe 4 - Sensor auslesen und Daten an den MQTT Broker schicken
import time
import ssl
import socketpool
import wifi
import json
import board
import busio

from jled import JLed
from adafruit_bmp280 import Adafruit_BMP280_I2C as BMP280
from adafruit_minimqtt import adafruit_minimqtt as MQTT
from TM1637 import TM1637

# Add a secrets.py to your filesystem that has a dictionary called secrets with
# "ssid" and "password" keys with your WiFi credentials. DO NOT share that file
# or commit it into Git or other source control.
# pylint: disable=no-name-in-module,wrong-import-order
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# BMP280 sensor connected to I²C pins GP16 (SDA) and GP17 (SCL)
#i2c = busio.I2C(board.GP17, board.GP16)
#sensor = BMP280(i2c, 118)
from collections import namedtuple
Sensor=namedtuple("Sensor", ("temperature","pressure"))
sensor=Sensor(22, 1001)
display = TM1637(board.GP14,board.GP15)
statusLED = JLed(board.GP2)
counter = 1

# Auf diesem Topic sendet der Client seine Messungen an das Backend
# Format: { "temperature": 22.0, "pressure": 1024 , "deviceid": "abcdef"}
temperature_topic = "iotlabclt23/" + secrets["deviceid"] + "/temperature"

# Auf diesem Topic empfängt der Client Acknwoledgements vom Backend
ack_topic = "iotlabclt23/" + secrets["deviceid"] + "/ack"

def connect_to_wifi(ssid, password):
    print(f"Connecting to WIFI {ssid}")
    wifi.radio.connect(ssid, password)
    print(f"Connected to {ssid}!")


def mqtt_on_connect(client, userdata, flags, rc):
    # This function will be called when the client is connected successfully to the broker.
    print("Connected to MQTT broker")
    # Wir möchten Nachrichten vom Backend auf dem Topic ack_topic empfangen
    client.subscribe(ack_topic)


def mqtt_on_disconnect(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from MQTT broker")


def mqtt_on_message(client, topic, message):
    # Diese Methode wird aufgerufen, wenn wir eine Nachricht empfangen
    print(f"New message on topic {topic}: {message}")
    # Effekt für Status LED setzen
    statusLED.fade_off(750)


def connect_to_mqtt_broker(broker, port):
    # Set up a MQTT Client
    mqtt_client = MQTT.MQTT(
        broker=broker,
        port=port,
        username="",
        password="",
        socket_pool=socketpool.SocketPool(wifi.radio),
        ssl_context=ssl.create_default_context(),
    )

    # Setup the callback methods above
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_disconnect = mqtt_on_disconnect
    mqtt_client.on_message = mqtt_on_message

    # Connect the client to the MQTT broker.
    print(f"Connecting to mqtt://{broker}:{port}...")
    mqtt_client.connect()
    return mqtt_client

def sensor_lesen(sensor):
    """temperatur und druck vom sensor lesen und als tupel zurückgeben"""
    return sensor.temperature, sensor.pressure


def daten_ausgeben(display, counter, temperature, pressure):
    """Daten auf der Konsole und dem Display ausgeben"""
    print(f"{counter} - {temperature:.2f} °C, {pressure:.2f} hPa")
    display.temperature(round(temperature))


def daten_senden(mqtt_client, counter, temperature, pressure, deviceid):
    """Daten in JSON-nachricht verpacken und per MQTT versenden"""
    message  = json.dumps({"temperature": temperature, 
                           "pressure": pressure, 
                           "deviceid": deviceid})
    print(f"{counter} - Sending message: {message} to {temperature_topic}...")
    mqtt_client.publish(temperature_topic, message)


connect_to_wifi(secrets['ssid'], secrets['password'])
mqtt_client = connect_to_mqtt_broker(secrets['broker'], secrets['port'])
last = 0

while True:
    # MQTT message queue pollen
    mqtt_client.loop()
    # Status LED aktualisieren
    statusLED.update()

    # alle 5 Sekunden Sensor lesen und Daten senden und ausgeben
    now = time.monotonic()
    if now - last > 5:
        last = time.monotonic()
        temperature, pressure = sensor_lesen(sensor)
        daten_ausgeben(display, counter, temperature, pressure)
        daten_senden(mqtt_client, counter, temperature, pressure, secrets["deviceid"])
        counter += 1

