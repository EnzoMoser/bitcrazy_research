"""
Simple example that connects to the crazyflie at `URI` and writes to
parameters that control the LED-ring,
it has been tested with (and designed for) the LED-ring deck.

Change the URI variable to your Crazyflie configuration.
"""
import logging
import time

import cflib.crtp
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.utils import uri_helper

# URI to the Crazyflie to connect to
URI = uri_helper.uri_from_env(default='radio://1/80/2M/EE5C21CFA8')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)


if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    with SyncCrazyflie(URI) as scf:
        cf = scf.cf

        # Set solid color effect
        cf.param.set_value('ring.effect', '7')
        # Set the RGB values
        cf.param.set_value('ring.solidRed', '100')
        cf.param.set_value('ring.solidGreen', '0')
        cf.param.set_value('ring.solidBlue', '0')
        time.sleep(2)

        # Set black color effect
        cf.param.set_value('ring.effect', '0')
        time.sleep(1)

        # Set fade to color effect
        cf.param.set_value('ring.effect', '14')
        # Set fade time i seconds
        cf.param.set_value('ring.fadeTime', '1.0')
        # Set the RGB values in one uint32 0xRRGGBB
        cf.param.set_value('ring.fadeColor', int('0000A0', 16))
        time.sleep(1)
        cf.param.set_value('ring.fadeColor', int('00A000', 16))
        time.sleep(1)
        cf.param.set_value('ring.fadeColor', int('A00000', 16))
        time.sleep(1)
