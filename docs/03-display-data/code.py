# Temperaturwerte und Luftdruck von einem BMP280 sensor, der über I²C
# angeschlossen ist, auslesen und auf einem TM1637 7-Segment-Display ausgeben
import busio
import board
import time

from adafruit_bmp280 import Adafruit_BMP280_I2C as BMP280
from TM1637 import TM1637

i2c = busio.I2C(board.GP17, board.GP16)
sensor = BMP280(i2c, 118)
display = TM1637(board.GP14,board.GP15)
counter = 1

def sensor_lesen(sensor):
    """temperatur und druck vom sensor lesen und als tupel zurückgeben"""
    return sensor.temperature, sensor.pressure

def daten_ausgeben(display, counter, temperature, pressure):
    """daten auf der Konsole und dem Display ausgeben"""
    print(f"{counter} - {temperature:.2f} °C, {pressure:.2f} hPa")
    display.temperature(round(temperature))

while True:
    temperature, pressure = sensor_lesen(sensor)
    daten_ausgeben(display, counter, temperature, pressure)
    time.sleep(1)
    counter += 1
