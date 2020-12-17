from shifter import shifter595
from time import sleep

test_runs = 10
test_first_n_switches = 1  # max 8
pause = 0.5
s = shifter595()

s.clear_all_registers()
sleep(pause)

for x in range(0, test_runs):
    for n in range(0, test_first_n_switches):
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



