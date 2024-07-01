# GNU General Public License

"""
This script moves the drone forward until it detects the color black.
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

import atexit
import sys

# URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/80/2M/EE5C21CFA6')

# Only output errors from the logging framework
logging.basicConfig(level=logging.ERROR)

# Python does not have constants. 
log_check_in_ms = 81
log_check = log_check_in_ms / 1000
wait_time = log_check*1.3    # Time to wait before checking log.
flying_height = 0.1 # In meters
shutter_speed_lim = 3000     # Shutter speed is between 0 and 8000. If the shutter speed is above shutter_speed_lim, the color below is black.
tolerance_radius = 0.02     # In meters. The desired drone coords must be within this radius
accel_tol = 0.02

# Initialize the low-level drivers
cflib.crtp.init_drivers()

# Add resources to the context manager for the duration of the script
def add_to_context_manager(target):
    enter = type(target).__enter__
    exit = type(target).__exit__
    value = enter(target)
    hit_except = False
    item = None
    try:
        item = value
    except:
        hit_except = True
        if not exit(target, *sys.exc_info()):
            raise
    if not hit_except:
        def leave_target():
            exit(target, None, None, None)
        # The target will only leave context manager if interrupted.
        atexit.register( leave_target )
    return item

# Connect to Crazyflie
scf = add_to_context_manager( SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) )
# Setup the position commander. Will fly up once initialized. Will land once the script exits.
pc = add_to_context_manager( PositionHlCommander(scf, controller=PositionHlCommander.CONTROLLER_PID) )
pc.set_default_height(0.1) # Default height in meters
pc.set_default_velocity(0.15) # Default velocity in m/s

# Make sure to manually exit, otherwise the script will keep running.
def manual_exit():
    if 'pc' in globals():
        pc.__exit__(*sys.exc_info() )
    if 'scf' in globals():
        scf.__exit__(*sys.exc_info() )
atexit.register( manual_exit )

##### Create log configuration
are_we_logging = False
def is_logging():
    return are_we_logging
lg_stab = LogConfig(name='Light_Level_At_Location', period_in_ms=log_check_in_ms)
lg_stab.add_variable('motion.shutter', 'uint16_t')
lg_stab.add_variable('stateEstimateZ.x', 'int16_t')
lg_stab.add_variable('stateEstimateZ.y', 'int16_t')
lg_stab.add_variable('stateEstimateZ.z', 'int16_t')
lg_stab.add_variable('stateEstimateZ.vx', 'int16_t')
lg_stab.add_variable('stateEstimateZ.vy', 'int16_t')

def start_log():
    scf.cf.log.reset()
    scf.cf.log.add_config(logconf)
    logconf.data_received_cb.add_callback(log_stab_callback)
    logconf.start()

# Grab data and put into globals
def log_stab_callback(timestamp, data, _):
    global globX, globY, globZ, globVx, globVy, globShut, are_we_logging
    # Coords
    globX = np.int16(data['stateEstimateZ.x']) 
    globY = np.int16(data['stateEstimateZ.y'])
    globZ = np.int16(data['stateEstimateZ.z'])
    # Acceleration
    globVx = np.int16(data['stateEstimateZ.vx']) 
    globVy = np.int16(data['stateEstimateZ.vy'])
    # Shutter speed (Detects light)
    globShut = np.uint16(data['motion.shutter'])
    are_we_logging = True

logconf = lg_stab
logconf_callback = log_stab_callback
start_log() # Start logging
######

## Grab globals and return in correct format
def grab_shut():
    return np.uint16(globShut)
def grab_vx_vy():
    return np.float16(globVx/1000), np.float16(globVy/1000)
def grab_x_y():
    return np.float16(globX/1000), np.float16(globY/1000)
def grab_x_y_z():
    return np.float16(globX/1000), np.float16(globY/1000), np.float16(globZ/1000)
def grab_x_y_z_shut():
    return np.float16(globX/1000), np.float16(globY/1000), np.float16(globZ/1000), np.uint16(globShut)
def grab_x_y_vx_vy():
    return np.float16(globX/1000), np.float16(globY/1000), np.float16(globVx/1000), np.float16(globVy/1000)
def grab_x_y_vx_vy_shut():
    return np.float16(globX/1000), np.float16(globY/1000), np.float16(globVx/1000), np.float16(globVy/1000), np.uint16(globShut)
def grab_x_y_z_vx_vy_shut():
    return np.float16(globX/1000), np.float16(globY/1000), np.float16(globZ/1000), np.float16(globVx/1000), np.float16(globVy/1000), np.uint16(globShut)

def print_x_y_z_vx_vy_shut():
    x, y, z, vx, vy, shut = grab_x_y_z_vx_vy_shut()
    print("X: %.2f\tY: %.2f\tZ: %.2f\tVx: %.2f\tVy: %.2f\tShut: %d" % ( x, y, z, vx, vy, shut ) )

def mov(new_x, new_y):
    pc.go_to(new_x, new_y)
    time.sleep(wait_time)
    x, y, vx, vy, shut = grab_x_y_vx_vy_shut()
    while abs(x - new_x) > tolerance_radius or abs(y - new_y) > tolerance_radius or abs(vx) > accel_tol or abs(vy) > accel_tol:
        pc.go_to(new_x, new_y)
        time.sleep(wait_time)
        x, y, vx, vy, shut = grab_x_y_vx_vy_shut()
        if shut > shutter_speed_lim:
            color_black = True
        else:
            color_black = False
    return x, y, color_black

if __name__ == '__main__':
    print("You are NOT supposed to run this!")


