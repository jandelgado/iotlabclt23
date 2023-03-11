import time
import board
import digitalio

led_rot = digitalio.DigitalInOut(board.GP2)
led_rot.direction = digitalio.Direction.OUTPUT
led_gelb = digitalio.DigitalInOut(board.GP3)
led_gelb.direction = digitalio.Direction.OUTPUT
value = True

while True:
    led_rot.value = value
    led_gelb.value = not value
    value = not value
    time.sleep(0.5)

