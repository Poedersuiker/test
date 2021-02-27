import gpiozero
import time

coil_A_1_pin = gpiozero.DigitalOutputDevice(6)
coil_A_2_pin = gpiozero.DigitalOutputDevice(13)
coil_B_1_pin = gpiozero.DigitalOutputDevice(19)
coil_B_2_pin = gpiozero.DigitalOutputDevice(26)


def forward(delay, steps):
    i = 0
    while i in range(0, steps):
        setStep(1, 0, 0, 0)
        time.sleep(delay)
        setStep(1, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 0, 0)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 0)
        time.sleep(delay)
        setStep(0, 0, 1, 1)
        time.sleep(delay)
        setStep(0, 0, 0, 1)
        time.sleep(delay)
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        i += 1


def backwards(delay, steps):
    i = 0
    while i in range(0, steps):
        setStep(1, 0, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 0, 1)
        time.sleep(delay)
        setStep(0, 1, 1, 0)
        time.sleep(delay)
        setStep(1, 0, 1, 0)
        time.sleep(delay)
        i += 1


def setStep(w1, w2, w3, w4):
    if w1:
        coil_A_1_pin.on()
    else:
        coil_A_1_pin.off()

    if w2:
        coil_A_2_pin.on()
    else:
        coil_A_2_pin.off()

    if w3:
        coil_B_1_pin.on()
    else:
        coil_B_1_pin.off()

    if w4:
        coil_B_2_pin.on()
    else:
        coil_B_2_pin.off()


while True:
    user_delay = input("Delay between steps (milliseconds)?")
    user_steps = input("How many steps forward? ")
    forward(int(user_delay) / 1000.0, int(user_steps))
    user_steps = input("How many steps backwards? ")
    backwards(int(user_delay) / 1000.0, int(user_steps))
