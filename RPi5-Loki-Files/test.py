import gpiozero as gz
import time

print("Hello There")

status, count = 0
led = gz.LED(16)

while(count < 10):
    led.toggle()