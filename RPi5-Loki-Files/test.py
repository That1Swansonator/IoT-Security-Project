import gpiozero as gz
import time

print("Hello There")

led = gz.LED(17)
led.on();