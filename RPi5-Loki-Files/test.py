# Import necessary modules
import gpiod
import time

# Define GPIO chip and line numbers
CHIP = "gpiochip0"  # Change to the appropriate chip name
LINE_NUM = 17       # GPIO 17

# Open the GPIO chip
chip = gpiod.Chip(CHIP)

# Get the GPIO line
line = chip.get_line(LINE_NUM)

# Request the line for output
line.request(consumer="my-led", type=gpiod.LINE_REQ_DIR_OUT)

try:
    while True:
        # Toggle the LED
        line.set_value(1)
        time.sleep(1)
        line.set_value(0)
        time.sleep(1)
except KeyboardInterrupt:
    # Clean up
    line.release()
    chip.close()
