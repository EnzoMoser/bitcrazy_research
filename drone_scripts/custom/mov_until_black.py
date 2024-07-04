# GNU General Public License

"""
Requires the Flow Deck. This script moves the drone forward until it detects the color black.
"""

import time
import numpy as np

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncLogger import SyncLogger

from cflib.positioning.position_hl_commander import PositionHlCommander

from cflib.utils import uri_helper
import logging

# URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/80/2M/EE5C21CFA6')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

def log_stab_callback(timestamp, data, logconf):
    global globX, globY, globZ, glogAx, globAy, globShut
    # Coords
    globX = np.int16(data['stateEstimateZ.x']) 
    globY = np.int16(data['stateEstimateZ.y'])
    globZ = np.int16(data['stateEstimateZ.z'])
    # Acceleration
    globAx = np.int16(data['stateEstimateZ.ax']) 
    globAy = np.int16(data['stateEstimateZ.ay'])
    # Shutter speed (Detects light)
    globShut = np.uint16(data['motion.shutter'])

def grab_x_y():
    global globX, globY
    return np.float16(globX/1000), np.float16(globY/1000)

def grab_x_y_z():
    global globX, globY, globZ
    return np.float16(globX/1000), np.float16(globY/1000), np.float16(globZ/1000)

def grab_x_y_z_shut():
    global globX, globY, globZ, globShut
    return np.float16(globX/1000), np.float16(globY/1000), np.float16(globZ/1000), np.uint16(globShut)

def grab_x_y_z_ax_ay_shut():
    global globX, globY, globZ, globAx, globAy, globShut
    return np.float16(globX/1000), np.float16(globY/1000), np.float16(globZ/1000), np.float16(globAx/1000), np.float16(globAy/1000), np.uint16(globShut)

def black_or_white(last_color_white):
    x, y, z, shut = grab_x_y_z_shut()
    print("X: %.2f\tShut: %d" % ( x, shut ) )
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

def mov_to(pc, x, y, z):
    cur_x, cur_y, cur_z, _ = grab_x_y_z_shut()
    
def mov_until_black(scf, pc, logconf):
    cf = scf.cf
    cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()
    
    time.sleep(0.3)
    pc.go_to(0.0, 0.0, 0.5)
    time.sleep(0.3)
    x, y, _, _ = grab_x_y_z_shut()
    pc.go_to(x, y, 0.3)
    time.sleep(0.3)
    pc.go_to(x, y, 0.1)

    x = 0
    last_color_white = True
    while last_color_white:
        print("X: %.2f" % x)
        pc.go_to(x, y, 0.1)
        time.sleep(0.1)
        last_color_white = black_or_white(last_color_white)
        x = x + 0.01
    pc.go_to(x, y, 0.05)
    logconf.stop()

(...)

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers()

    lg_stab = LogConfig(name='Light_Level_At_Location', period_in_ms=81)
    lg_stab.add_variable('motion.shutter', 'uint16_t')
    lg_stab.add_variable('stateEstimateZ.x', 'int16_t')
    lg_stab.add_variable('stateEstimateZ.y', 'int16_t')
    lg_stab.add_variable('stateEstimateZ.z', 'int16_t')

    lg_stab.add_variable('stateEstimateZ.ax', 'int16_t')
    lg_stab.add_variable('stateEstimateZ.ay', 'int16_t')

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
        with PositionHlCommander(scf, controller=PositionHlCommander.CONTROLLER_PID) as pc:
            mov_until_black(scf, pc, lg_stab)


