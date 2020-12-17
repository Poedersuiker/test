from shifter import shifter595
from time import sleep

pause = 0.5
s = shifter595()

s.clear_all_registers()
sleep(pause)

for n in range(0, 8):
    # reset switch
    s.registers[1][n] = 1
    s.registers[0][n] = 0
    s.load_values()
    sleep(pause)

    s.registers[1][n] = 0
    s.registers[0][n] = 1
    s.load_values()
    sleep(pause)

    s.registers[1][n] = 1
    s.registers[0][n] = 1
    s.load_values()
    sleep(pause)

    s.registers[1][n] = 0
    s.registers[0][n] = 0
    s.load_values()
    sleep(pause)

s.clear_all_registers()



