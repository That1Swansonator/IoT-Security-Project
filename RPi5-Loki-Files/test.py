from time import sleep
import gpiozero

try:
    # Create a new LED object from the GPIO Zero library and assign it to the variable led at pin 17
    # GPIO17 pin, not BCM17 pin
    led = gpiozero.LED(17)

    # blink the LED on and off every 1 second
    for i in range(10):
        led.blink(on_time=1, off_time=1)
        sleep(5)
except Exception as e:
    print(f"An error occurred: {e}")


