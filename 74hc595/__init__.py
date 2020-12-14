from gpiozero import DigitalOutputDevice
from time import sleep


class shifter:
    def __init__(self):
        self.latch_pin = DigitalOutputDevice(16)
        self.clock_pin = DigitalOutputDevice(20)
        self.data_pin = DigitalOutputDevice(21)

        self.pause = 0

    def tick(self):
        self.clock_pin.on()
        sleep(self.pause)
        self.clock_pin.off()
        sleep(self.pause)

    def set_value(self, value):
        for i in range(24):
            bitwise = 0x800000 >> i
            bit = bitwise & value
            if bit == 0:
                self.data_pin.off()
            else:
                self.data_pin.on()
            self.tick()

    def clear(self):
        self.latch_pin.off()
        self.tick()
        self.latch_pin.on()

