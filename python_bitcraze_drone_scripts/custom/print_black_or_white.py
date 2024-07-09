# GNU General Public License

"""
Requires Flow Deck. Prints black or white based on shutter speed.
Does not fly, so you can hold the drone when doing this.
"""

import logging
import time
import numpy as np

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

# URI to the Crazyflie to connect to
uri = 'radio://0/80/2M/EE5C21CFA6'

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def log_stab_callback(timestamp, data, logconf):
    global globX, globY, globZ, globShut
    globX = np.int16(data['stateEstimateZ.x']) 
    globY = np.int16(data['stateEstimateZ.y'])
    globZ = np.int16(data['stateEstimateZ.z'])
    globShut = np.uint16(data['motion.shutter'])


def grab_log_values():
    global globX, globY, globZ, globShut
    return globX, globY, globZ, globShut

def black_or_white(last_color_white):
    x, y, z, shut = grab_log_values()
#    print(shut)
    if shut > 4000:
        cur_color_white = False
    else:
        cur_color_white = True
    if cur_color_white != last_color_white:
        if cur_color_white:
            print("White!")
        else:
            print("Black!")
    return cur_color_white

def simple_log_async(scf, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    last_color_white = True
    while True:
        time.sleep(0.25)
        last_color_white = black_or_white(last_color_white)
    logconf.stop()

(...)

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Light_Level_At_Location', period_in_ms=200)
    lg_stab.add_variable('motion.shutter', 'uint16_t')
    lg_stab.add_variable('stateEstimateZ.x', 'int16_t')
    lg_stab.add_variable('stateEstimateZ.y', 'int16_t')
    lg_stab.add_variable('stateEstimateZ.z', 'int16_t')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:

        simple_log_async(scf, lg_stab)

