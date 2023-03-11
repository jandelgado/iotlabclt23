# Aufgabe 4 - Sensor auslesen und Daten an den MQTT Broker schicken
import time
import ssl
import socketpool
import wifi
import json
import board
import busio
from secrets import secrets

from adafruit_bmp280 import Adafruit_BMP280_I2C as BMP280
from adafruit_minimqtt import adafruit_minimqtt as MQTT
from TM1637 import TM1637

# BMP280 sensor connected to I²C pins GP16 (SDA) and GP17 (SCL)
i2c = busio.I2C(board.GP17, board.GP16)
sensor = BMP280(i2c, 118)
display = TM1637(board.GP14,board.GP15)
counter = 1

# Auf diesem Topic sendet der Client seine Messungen an das Backend
# Format: { "temperature": 22.0, "pressure": 1024 , "deviceid": "abcdef"}
temperature_topic = "iotlabclt23/" + secrets["deviceid"] + "/temperature"

def connect_to_wifi(ssid, password):
    print(f"Connecting to WIFI {ssid}")
    wifi.radio.connect(ssid, password)
    print(f"Connected to {ssid}!")

def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")

def mqtt_on_disconnect(client, userdata, rc):
    print("Disconnected from MQTT broker")

def connect_to_mqtt_broker(broker, port):
    # MQTT client definieren
    mqtt_client = MQTT.MQTT(
        broker=broker,
        port=port,
        username="",
        password="",
        socket_pool=socketpool.SocketPool(wifi.radio),
        ssl_context=ssl.create_default_context(),
    )

    # Callbacks installieren
    mqtt_client.on_connect = mqtt_on_connect
    mqtt_client.on_disconnect = mqtt_on_disconnect

    print(f"Connecting to mqtt://{broker}:{port}...")
    mqtt_client.connect()
    return mqtt_client


def daten_senden(mqtt_client, counter, temperature, pressure, deviceid):
    """Daten in JSON-Nachricht verpacken und per MQTT versenden"""
    message  = json.dumps({"temperature": temperature, 
                           "pressure": pressure, 
                           "deviceid": deviceid})
    print(f"{counter} - Sending message: {message} to {temperature_topic}...")
    mqtt_client.publish(temperature_topic, message)

##############################################################################
## TODO Funktionen sensor_lesen und daten_ausgeben hier eingügen            ##
##############################################################################

connect_to_wifi(secrets['ssid'], secrets['password'])
mqtt_client = connect_to_mqtt_broker(secrets['broker'], secrets['port'])
last = 0

while True:
    # MQTT message queue pollen
    mqtt_client.loop()

    # alle 5 Sekunden Sensor lesen und Daten senden und ausgeben
    now = time.monotonic()
    if now - last > 5:
        last = time.monotonic()
        counter += 1
##############################################################################
## TODO Funktionen sensor_lesen, daten_ausgeben  und daten_senden           ##
##      hier aufrufen                                                       ##
##############################################################################
        temperature, pressure = ...

