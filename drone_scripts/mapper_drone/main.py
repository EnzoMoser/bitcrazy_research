import control_real_drone as dn
import sys
import time

while not dn.is_logging():
    time.sleep(0.5)


def move(go_x, go_y):
    x, y, cor = dn.mov(go_x, go_y)
    if cor == True:
        color = "Black"
    else:
        color = "White"
    print("X:", x, "Y:", y, "Cor:", color)
    return x, y, cor

move(0.1, 0.1)
move(0.2, 0.0)
move(0.3, -0.1)
move(0.2, 0.0)

dn.manual_exit()
