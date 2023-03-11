from jled import JLed
import board

led1 = JLed(board.GP2).fade_on(1000).forever()
led2 = JLed(board.GP3).blink(250,750).forever()

while True:
    led1.update()
    led2.update()

