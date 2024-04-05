# Import necessary modules
import gpiod
import time

# Define GPIO chip and line numbers
CHIP = "/dev/gpiochip0"  # Change to the appropriate chip name
LINE_NUM = 17  # GPIO 17

# Open the GPIO chip
# chip = gpiod.Chip(CHIP)

with gpiod.Chip(CHIP) as chip:
    # The chip is automatically opened here & You can use the chip within this context
    led = chip.get_line(LINE_NUM)

    config = gpiod.line_request
    config.consumer = "Blink"
    config.request_type = gpiod.line_request.DIRECTION_OUTPUT
    #config.type = gpiod.LINE_REQ_DIR_OUT

    led.request(config)

    print(led.consumer)

    while True:
        led.set_value(0)
        time.sleep(0.1)
        led.set_value(1)
        time.sleep(0.1)

    pass

