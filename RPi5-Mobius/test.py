from time import sleep
import gpiozero

# Create a new LED object from the GPIO Zero library and assign it to the variable led at pin 17
# GPIO17 pin is connected to the LED on the Mobius board
led = gpiozero.LED(17)

# Turn the LED off for 10 seconds
led.off()
sleep(10)
led.on()
