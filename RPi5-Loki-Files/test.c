//
// Created by patrick on 4/9/24.
//

#include <unistd.h>
#include "stdio.h"
#include "stdlib.h"
#include "gpiod.h"



int main(void){

    struct gpiod_chip *chip;
    struct gpiod_line *lineGreen;  // Green LED


    // select the chip gpiochip1
    chip = gpiod_chip_open("/dev/gpiochip1");

    if (chip == NULL) {
        printf("Failed to open chip\n");
        return EXIT_FAILURE;
    }

    // get the line 17
    lineGreen = gpiod_chip_get_line(chip, 27);

    if (lineGreen == NULL) {
        printf("Failed to get line\n");
        gpiod_chip_close(chip);
        return EXIT_FAILURE;
    }

    // request the line
    gpiod_line_request_output(lineGreen, "example1", 0);

    // blink the LED
    for (int i = 0; i < 10; i++) {
        gpiod_line_set_value(lineGreen, 1);
        sleep(1);
        gpiod_line_set_value(lineGreen, 0);
        sleep(1);
    }

    // close the line
    gpiod_line_release(lineGreen);

    //close the chip
    gpiod_chip_close(chip);

    return EXIT_SUCCESS;
}
