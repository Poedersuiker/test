from shifter import shifter595
from time import sleep

test_runs = 10
pause = 0.1
s = shifter595()

s.clear_all_registers()
sleep(pause)

for x in range(0, test_runs):
    for i in range(0, 2):
        for n in range(0, 8):
            s.clear_all_registers()
            s.registers[i][n] = 1
            s.load_values()
            s.latch()
            sleep(pause)


