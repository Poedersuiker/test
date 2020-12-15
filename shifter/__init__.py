from gpiozero import DigitalOutputDevice
from time import sleep


class shifter595:
    def __init__(self, chain=2):
        self.chain = chain  # number of chips in a row

        self.registers = []
        for i in range(0, self.chain):
            self.registers.append([0, 0, 0, 0, 0, 0, 0, 0])

        self.latch_pin = DigitalOutputDevice(16)
        self.clock_pin = DigitalOutputDevice(20)
        self.data_pin = DigitalOutputDevice(21)

        self.pause = 0

    def tick(self):
        self.clock_pin.on()
        sleep(self.pause)
        self.clock_pin.off()
        sleep(self.pause)

    def set_value(self):
        for i in range(0, self.chain):
            for n in range(0, 8): # 74hc595 has 8 outputs
                bit = self.registers[i][n]
                if bit == 0:
                    self.data_pin.off()
                else:
                    self.data_pin.on()
                self.tick()

    def latch(self):
        self.latch_pin.off()
        sleep(self.pause)
        self.latch_pin.on()

