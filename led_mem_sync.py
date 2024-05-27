"""
Simple example that connects to the crazyflie at `URI` and writes to
the LED memory so that individual leds in the LED-ring can be set,
it has been tested with (and designed for) the LED-ring deck.

Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

URI = uri_helper.uri_from_env(default='radio://0/80/2M/EE5C21CFA8')


def set_color(start_led, end_led, red, green, blue):
    mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
    for i in range(start_led, end_led+1):
        mem[0].leds[i].set(r=red, g=green, b=blue)

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        # Set virtual mem effect effect
        cf.param.set_value('ring.effect', '13')

        # Get LED memory and write to it
        mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
        if len(mem) > 0:
            set_color(0, 2, 100, 0, 0)
            set_color(3, 5, 0, 100, 0)
            set_color(6, 8, 0, 0, 100)
            set_color(9, 11, 100, 100, 100)
            mem[0].write_data(None)
        time.sleep(0.5)
