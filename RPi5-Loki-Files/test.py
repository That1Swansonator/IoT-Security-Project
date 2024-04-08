from time import sleep

import gpiozero

# Create a new LED object from the GPIO Zero library and assign it to the variable led at pin 2 and a ground pin
led = gpiozero.LED(11)

# blink the LED on and off every 1 second
for i in range(10):
    led.blink(on_time=1, off_time=1)
    sleep(5)



