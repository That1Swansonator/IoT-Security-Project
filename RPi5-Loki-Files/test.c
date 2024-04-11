//
// Created by patrick on 4/9/24.
//

#include <unistd.h>
#include "stdio.h"
#include "stdlib.h"
#include "gpiod.h"


int main(void){
    // select the chip gpiochip0
    struct gpiod_chip *chip = gpiod_chip_open("/dev/gpiochip0");

    if (!chip) {
        perror("Open chip failed\n");
        return EXIT_FAILURE;
    }

    // get the line 17
    struct gpiod_line *line = gpiod_chip_get_line(chip, 17);

    if (!line) {
        perror("Get line failed\n");
        return EXIT_FAILURE;
    }

    // blink the LED
    for (int i = 0; i < 10; i++) {
        gpiod_line_set_value(line, 1);
        sleep(1);
        gpiod_line_set_value(line, 0);
        sleep(1);
    }

    // close the line
    gpiod_line_release(line);
    //close the chip
    gpiod_chip_close(chip);

    return EXIT_SUCCESS;
}