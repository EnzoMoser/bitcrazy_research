# GNU General Public License

"""
This script handles the mapping of an area, and the creation and following of a path between two points.
This script relies on another script to actually handle the low-level drone communication...
This means one could replace the low-level drone for a fake drone script in order to simulate the drone...
A fully working simulation was made in Matlab. Pieces of that simulation was used as a reference for some of the Python code below.

This script does two things. You can run the script twice to see it in effect:

1.
    If a certain png file is not available in the directory, it will:
    - Map out the area underneath based on the light levels, marking white as crossable area.
    - Then, it will look for a crossable area to mark as an endpoint.
    - And it will save this new image as the png.
    - It will then end the script. 
2.
    If a png file with a certain name is available, it will:
    - Create a path between the start and end points seen on the map.
    - It will follow this path, and readjust automatically for any dynamic obstacles.
    - The script will not stop. It will then move between these two points forever, or until it is forcefully stopped, or if there is no path to take.
"""

import sys
import os
import atexit
import time
import numpy as np
import signal
from PIL import Image
import matplotlib.pyplot as plt
from collections import deque

REAL_DRONE = True           # Whether or not to use the script that controls the real drone.
USE_LOADED_IMAGE = True     # Whether or not to use a png file within the directory for the map, if available.
MOVE_LENGTH = np.float16(0.08) # In metres. How far the real drone moves to move one pixel in the visual image.

# Colors used for the visual map:
LINE_COLOR = (255, 255, 255)    # The drone can move here
BORDER_COLOR = (0, 0, 0)        # Mark solid uncrossable area
UNKNOWN_COLOR = (130, 130, 200) # Unknown area
NEW_OBSTACLE_COLOR = (255, 0, 0)# Dynamic obstacle area
DRONE_COLOR = (0, 255, 0)       # Drone color
BAD_DRONE_COLOR = (255, 0, 255) # Drone color when in uncrossable area
START_COLOR = (0, 255, 255)     # Where the drone starts
END_COLOR = (255, 255, 0)       # Where the drone should end

if REAL_DRONE:
    import control_real_drone as dn
else:
    # Here you could put a simulation script, i.e:
    # import control_fake_drone as dn
    pass

atexit.register( dn.manual_exit ) # Manually exit dn when this script exits.
def keyboard_interrupt_handler(signal, frame):
    dn.manual_exit()
    sys.exit(0)
signal.signal(signal.SIGINT, keyboard_interrupt_handler) # Add manually exit to 
print("Press Ctrl+C for Emergency Exit")


bad_colors = { BORDER_COLOR, UNKNOWN_COLOR, NEW_OBSTACLE_COLOR } # Put all the bad colors together

# Setup the matplotlib figure and axis
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
ax.imshow(Image.new('RGB', (20, 20), (255, 255, 255) ) )

# Move to this real coordinate from the absolute positioning system
def mov(new_drone_coord):
    x, y, is_black = dn.mov(new_drone_coord[0], new_drone_coord[1])
    global _drone_coord
    _drone_coord = new_drone_coord
    return not is_black

# Get the real coordinates from dn
def get_coords():
    x, y = dn.grab_x_y()
    return np.array( [x, y] )

# Display the image
def display_img(img):
    ax.clear()
    plt.minorticks_on()
    plt.grid(which='both', color='gray', linestyle='-', linewidth=0.2)
    # We need to specify the x and y in order to display the image correctly
    ax.set_xlim(0, img.height-1)
    ax.set_ylim(0, img.width-1)
    ax.imshow(img)
    plt.pause(0.005)  # The image must pause to update

# Display the drone
def display_drone(img, vis_drone_coord):
    drone_img = img.copy()
    set_pixel(drone_img, vis_drone_coord, DRONE_COLOR)
    display_img(drone_img)

# Display the drone with the bad color
def display_bad_drone(img, vis_drone_coord):
    drone_img = img.copy()
    set_pixel(drone_img, vis_drone_coord, BAD_DRONE_COLOR)
    display_img(drone_img)

# Set a pixel a certain color in the image using numpy array coordinates
def set_pixel(img, coords_numpy, color):
    coords_python = tuple(coords_numpy)
    img.putpixel(coords_python, color)

# Get the color of a pixel from a numpy array coordinate 
def get_pixel(img, coords_numpy):
    coords_python = tuple(coords_numpy)
    return img.getpixel(coords_python)

# Check if a coordinate is within bounds
def size_check(coord, max_num, min_num):
    if coord[0] < min_num:
        min_num = coord[0]
    elif coord[0] > max_num:
        max_num = coord[0]
    if coord[1] < min_num:
        min_num = coord[1]
    elif coord[1] > max_num:
        max_num = coord[1]
    return max_num, min_num

# Convert the coordinates from the real drone to the visual drone
def real_to_vis(real):
    vis = ( np.ceil( real * _rv_mult ) + _rv_off ).astype(int)
    return vis

# Convert the coordinates from the visual drone to the real drone
def vis_to_real(vis):
    real = ( (vis - _rv_off) / _rv_mult ).astype(float)
    return real

# Scan the area and return the newly created map
def scan_area( ):
    # The cardianl directions. The third value in each array is leftover from an older deprecated design. It could be removed, but more rewriting is then needed.
    dir = np.array( [ [1, 0, 0], [0, 1, 1], [-1, 0, 2], [0, -1, 3] ] )
    global _rv_mult, _rv_off, _vis_start, _vis_img, _vis_drone_coord, _vis_size

    vis_starting_size = 20 # Start with a square map of this length
    vis_increase_size = 2 # The factor at which the visual map size increases when it reaches the border
    vis_border = 2 # It needs a border of this many pixels to look nice
    _vis_size = vis_starting_size+int(np.ceil(2*vis_border))
    vis_start_coord = 1 + int(np.ceil(_vis_size / 2))
    _vis_drone_coord = np.array( [ vis_start_coord, vis_start_coord ] )
   
    vis_small = vis_border
    old_small = vis_small
    vis_big = _vis_size - vis_border
    old_big = vis_big    

    _vis_img = Image.new('RGB', (_vis_size, _vis_size), UNKNOWN_COLOR)
    start_drone_coord = _drone_coord
    set_pixel(_vis_img, _vis_drone_coord, START_COLOR) # Place the starting coordinate where the drone starts
    display_drone(_vis_img, _vis_drone_coord)

    _rv_mult = np.float32( 1 / MOVE_LENGTH ) # Multiplier
    _rv_off = _vis_drone_coord - np.multiply(_drone_coord, _rv_mult) # Array offset

    # Keep a stack of coordinates to visit
    stack = np.array( [ [ _vis_drone_coord[0], _vis_drone_coord[1], 4 ] ] ) # The third value is deprecated

    while stack.shape[0] > 0:        
        da_list = dir + np.array( [ stack[-1, 0 ], stack[-1, 1 ], 0 ] )
        next_coord = np.array( [] )
        for i in range(4):
            # Look at the pixels around this coordinate

            ############### Check image sizes
            specific_coord = da_list[i]
            
            vis_big, vis_small = size_check(specific_coord, vis_big, vis_small)
            if vis_big > old_big or vis_small < old_small:
                new_vis_size = int(np.ceil(_vis_size * vis_increase_size))
                new_vis_img = Image.new('RGB', (new_vis_size, new_vis_size), UNKNOWN_COLOR)
                add_to_offset = int(np.ceil( (new_vis_size - _vis_size)/4 ))
                st = add_to_offset

                new_vis_img.paste(_vis_img, (st, st) )

                _vis_img = new_vis_img
                _vis_drone_coord = _vis_drone_coord + add_to_offset
                stack[:, :2] = stack[:, :2] + add_to_offset
                _rv_off = _rv_off + add_to_offset
                _vis_size = new_vis_size
                vis_small = vis_border
                vis_big = new_vis_size - vis_border
                specific_coord[:2] = specific_coord[:2] + add_to_offset
                old_big = vis_big
                old_small = vis_small
                display_drone(_vis_img, _vis_drone_coord)
            ###########

            cor = get_pixel(_vis_img, da_list[i, :2])
            # If this pixel is unknwon, go and check it out
            if cor == UNKNOWN_COLOR:
                next_coord = da_list[i]
                break
            # If we have a pixel to check out, then check it out
        if next_coord.size > 0:
            test_drone_coord = vis_to_real(next_coord[:2])
            vis_test_drone_coord = next_coord[:2]

            is_crossable = mov(test_drone_coord)

            if is_crossable:
                _vis_drone_coord = vis_test_drone_coord
                # Since this pixel is crossable, we add it to the stack to check adjacent pixels.
                stack = np.append(stack, [ next_coord ], axis=0)
                use_color = LINE_COLOR
                display_drone(_vis_img, _vis_drone_coord)
            else:
                display_bad_drone(_vis_img, vis_test_drone_coord)
                use_color = BORDER_COLOR

            set_pixel(_vis_img, vis_test_drone_coord, use_color)
        else:
            # If no pixels adjacent to the coordinate were checked out, remove the coordinate from the stack.
            stack = np.delete(stack, -1, axis=0)

    ### Shrink the map
    # Get the first not unknown pixel from each side.
    # See which one has the closest and fathest coordinates.
    # Resize the map based on this info plus the visual border.

    # Convert to numpy arrays
    vis_arr = np.array(_vis_img)
    unk_arr = np.array(UNKNOWN_COLOR)

    # There is a better way to write this section.
    diff_cor = False
    diff_coord = -1
    j = 0
    while not diff_cor:
        i = 0
        while not diff_cor:
            if not (unk_arr == vis_arr[j, i] ).all():
                diff_cor = True
                diff_coord = j
                break
            i = i + 1
            if i >= _vis_size:
                break
        j = j + 1
        if j >= _vis_size:
            break

    first_row = diff_coord

    diff_cor = False
    diff_coord = -1
    j = _vis_size - 1
    while not diff_cor:
        i = 0
        while not diff_cor:
            if not (unk_arr == vis_arr[j, i] ).all():
                diff_cor = True
                diff_coord = j
                break
            i = i + 1
            if i >= _vis_size:
                break
        j = j - 1
        if j < 0:
            break

    last_row = diff_coord

    diff_cor = False
    diff_coord = -1
    j = 0
    while not diff_cor:
        i = 0
        while not diff_cor:
            if not (unk_arr == vis_arr[i, j] ).all():
                diff_cor = True
                diff_coord = j
                break
            i = i + 1
            if i >= _vis_size:
                break
        j = j + 1
        if j >= _vis_size:
            break

    first_col = diff_coord

    diff_cor = False
    diff_coord = -1
    j = _vis_size - 1
    while not diff_cor:
        i = 0
        while not diff_cor:
            if not (unk_arr == vis_arr[i, j] ).all():
                diff_cor = True
                diff_coord = j
                break
            i = i + 1
            if i >= _vis_size:
                break
        j = j - 1
        if j < 0:
            break

    last_col = diff_coord

    first = min(first_row, first_col)
    last = max(last_row, last_col)
    _vis_drone_coord = _vis_drone_coord - first + vis_border
    _rv_off = _rv_off - first + vis_border

    first_bor = first-vis_border
    last_bor = last+vis_border

    new_vis_arr = vis_arr[first_bor:(last_bor+1), first_bor:(last_bor+1)]

    _vis_img = Image.fromarray(new_vis_arr)
    _vis_size = _vis_img.width
    mov( start_drone_coord )
    _vis_drone_coord = real_to_vis(start_drone_coord)
    _vis_start = _vis_drone_coord
    display_drone(_vis_img, _vis_drone_coord)

# Return Manhatten distance
def get_dis(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

# Very basic script to create an end_point. Not ideal.
# It simply uses Manhatten distance to find...
# the futhest crossable pixel from the start_point
def create_end_point():
    line_arr = np.array(LINE_COLOR)
    vis_arr = np.array(_vis_img)
    max_d = 0
    point = np.array([])
    for i in range(_vis_size):
        for j in range(_vis_size):
            check_me = vis_arr[j, i]
            if (line_arr == check_me ).all():
                d = get_dis(_vis_start, np.array( [i, j] ))
                if d > max_d:
                    max_d = d
                    point = np.array([i, j])
    global _vis_end
    _vis_end = point
    if _vis_end.size <= 0:
        print("No End point!")
    else:
        print("End: ", _vis_end)
        set_pixel(_vis_img, _vis_end, END_COLOR)
    display_drone(_vis_img, _vis_drone_coord)

# Very basic BFS script. Not efficient nor ideal.
def bfs_path(img, start_coord, end_coord, b_colors):
    # Initialize the BFS queue
    queue = deque([start_coord])
    visited = set()
    visited.add(tuple(start_coord))
    
    # Dictionary to keep track of the path
    came_from = {}
    came_from[tuple(start_coord)] = None
    
    # Define the four cardinal directions
    directions = [np.array([1, 0]), np.array([-1, 0]), np.array([0, 1]), np.array([0, -1])]
    
    # Get image dimensions
    width, height = img.size
    
    while queue:
        current = queue.popleft()
        
        # Check if we have reached the end
        if np.array_equal(current, end_coord):
            path = []
            while current is not None:
                path.append(current)
                current = came_from[tuple(current)]
            return np.array(path[::-1])  # Return reversed path
        
        # Explore neighbors
        for direction in directions:
            neighbor = current + direction
            neighbor_tuple = tuple(neighbor)
            
            # Check bounds
            if (0 <= neighbor[0] < width) and (0 <= neighbor[1] < height):
                # Check if the neighbor is not a bad color and not visited
                da_pixel = img.getpixel((neighbor[0], neighbor[1]))
                if neighbor_tuple not in visited and da_pixel not in b_colors:
                    queue.append(neighbor)
                    visited.add(neighbor_tuple)
                    came_from[neighbor_tuple] = tuple(current)
    
    # Return None if no path is found
    return None

# Find the first instance of a color
def find_first_instance(img, color):
    arr = np.array(img)
    for y in range(img.height):
        for x in range(img.width):
            if (arr[y, x] == color).all():  # RGB value for white
                return np.array( [x, y] )
    
    # If no white pixel is found
    return None

# Use coordinates of the visual map to move the real drone.
def vis_mov(img, vis_coord):
    good_cor = mov ( vis_to_real(vis_coord) )
    global _vis_drone_coord
    _vis_drone_coord = vis_coord
    if good_cor:
        display_drone(img, _vis_drone_coord)
    else:
        display_bad_drone(img, _vis_drone_coord)
    return good_cor

# Move from start_point to end_point using basic BFS.
# If an obstacle is detected, it will mark it on the map and avoid it.
# If a new obstacle is detected after a successful loop,...
# it will assume the old obstacles are removed and will wipe the map of old obstacles before marking the new ones.
def mov_between_coords(temp_img, start_point, end_point):
    path = bfs_path(temp_img, start_point, end_point, bad_colors)
    vis_mov(temp_img, start_point)
    if path is None:
        print("No PATH! Cannot Move!")
        return False, temp_img
    new_temp = False
    old_coord = start_point
    while True:
        for coord in path:
            good_cor = vis_mov(temp_img, coord)
            if not ( (coord == start_point).all() or (coord == end_point).all() ):
                if not good_cor:
                    print("Blocked")
                    if not new_temp:
                        temp_img = _vis_img.copy()
                        new_temp = True
                    set_pixel(temp_img, coord, NEW_OBSTACLE_COLOR)
                    vis_mov(temp_img, old_coord)
                    start_point = old_coord
                    break
                else:
                    old_coord = coord
        if (_vis_drone_coord == end_point).all():
            return True, temp_img
        path = bfs_path(temp_img, start_point, end_point, bad_colors)
        if path is None:
            print("No PATH! Cannot Move!")
            return False, temp_img

# Unless all paths are blocked or you forcefully exit the script,...
# the drone will keep pathfinding and moving bewteen these two points indefinitely.
def loop_between_coords(start_point, end_point):
    _temp = _vis_img.copy()
    display_drone(_temp, _vis_drone_coord)
    while True:
        _rof, _temp = mov_between_coords(_temp, _vis_start, _vis_end)
        if not _rof:
            break
        _rof, _temp = mov_between_coords(_temp, _vis_end, _vis_start)
        if not _rof:
            break

# Wait for the drone to start logging before doing things
while not dn.is_logging():
    time.sleep(0.5)
time.sleep(0.5) # Wait for drone to initialize

# Get the real drone coords
time.sleep(0.2)
cake = get_coords()
mov(cake)
_drone_coord = get_coords()

# If there is a saved image, and we allow using saved images, don't bother scanning the area.
# Also,  
if USE_LOADED_IMAGE and os.path.isfile('vis_img.png'):
    dn.nice_shutter_speed() # Tell dn to use a nicer shutter speed
    _vis_img = Image.open('vis_img.png') # Load the map
    # Set all necessary globals:
    _vis_size = _vis_img.width
    _vis_start = find_first_instance(_vis_img, START_COLOR)
    _vis_end = find_first_instance(_vis_img, END_COLOR)
    _vis_drone_coord = _vis_start
    _rv_mult = np.float32( 1 / MOVE_LENGTH )
    _rv_off = _vis_drone_coord - np.multiply(_drone_coord, _rv_mult)

    # Move indefinitely between these two points
    loop_between_coords(_vis_start, _vis_end)
    
else:
    scan_area() # Create a map
    create_end_point() # Place an endpoint on the map
    _vis_img.save('vis_img.png') # Save this map
    # Stop moving

print("DONE!!!")
dn.manual_exit()
time.sleep(10) # Wait a bit so that we can admire the newly created map.