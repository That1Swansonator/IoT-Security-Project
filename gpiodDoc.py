>>> import gpiod
>>> help(gpiod)
>>> help(gpiod.chip)
>>> help(gpiod.line)
>>> help(gpiod.chip.open)

open(self, device, how:int=1)
    @brief Open a GPIO chip.

    @param device: String or int describing the GPIO chip.
    @param how:    Indicates how the chip should be opened.

    If the object already holds a reference to an open chip, it will be
    closed and the reference reset.

    Usage:
        chip.open("/dev/gpiochip0")
        chip.open(0, chip.OPEN_BY_NUMBER)