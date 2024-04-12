//
// Created by patrick on 4/9/24.
//

#include <unistd.h>
#include "stdio.h"
#include "stdlib.h"
#include "gpiod.h"
#include "gpiod.hpp"



int main(void){
    // select the chip gpiochip0
    struct gpiod_chip *chip = gpiod_chip_open("/dev/gpiochip0");



    if (!chip) {
        perror("Open chip failed\n");
        return EXIT_FAILURE;
    }

    // get the line 17
    struct gpiod_line *line = gpiod_chip_get_line(chip, 17);


    // blink the LED


    // close the line


    //close the chip
    gpiod_chip_close(chip);

    return EXIT_SUCCESS;
}