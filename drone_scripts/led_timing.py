"""
This example demonstrate the LEDTIMING led ring sequence memory. This memory and
led-ring effect allows to pre-program a LED sequence to be played autonomously
by the Crazyflie.

Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.mem import MemoryElement
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://0/80/2M/EE5C21CFA8')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI, cf=Crazyflie(rw_cache='./cache')) as scf:
        cf = scf.cf

        # Get LED memory and write to it
        mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LEDTIMING)
        if len(mem) > 0:
            mem[0].add(25, {'r': 100, 'g': 0, 'b': 0})
            mem[0].add(0, {'r': 0, 'g': 100, 'b': 0}, leds=1)
            mem[0].add(0, {'r': 0, 'g': 100, 'b': 0}, leds=2)
            mem[0].add(3000, {'r': 0, 'g': 100, 'b': 0}, leds=3, rotate=1)
            mem[0].add(50, {'r': 0, 'g': 0, 'b': 100}, leds=1)
            mem[0].add(25, {'r': 0, 'g': 0, 'b': 100}, leds=0, fade=True)
            mem[0].add(25, {'r': 100, 'g': 0, 'b': 100}, leds=1)
            mem[0].add(25, {'r': 100, 'g': 0, 'b': 0})
            mem[0].add(6000, {'r': 100, 'g': 0, 'b': 100})
            mem[0].write_data(None)
        else:
            print('No LED ring present')

        # Set virtual mem effect effect
        cf.param.set_value('ring.effect', '0')
        time.sleep(2)
        cf.param.set_value('ring.effect', '17')
        time.sleep(2)
