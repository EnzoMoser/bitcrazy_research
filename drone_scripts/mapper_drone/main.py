import control_real_drone as dn
import sys
import atexit
import time
import numpy as np
import signal
from PIL import Image
import matplotlib.pyplot as plt

atexit.register( dn.manual_exit )

def keyboard_interrupt_handler(signal, frame):
    dn.manual_exit()
    sys.exit(0)

signal.signal(signal.SIGINT, keyboard_interrupt_handler)
print("Press Ctrl+C for Emergency Exit")

move_length = np.float16(0.08) # Move length in meters

# Colors
border_color = (0, 0, 0)
line_color = (255, 255, 255)
unknown_color = (130, 130, 200)
drone_color = (255, 0, 255)
bad_drone_color = (200, 0, 150)
start_color = (0, 255, 255)
end_color = (255, 255, 0)

# Setup the matplotlib figure and axis
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
ax.imshow(Image.new('RGB', (20, 20), (255, 255, 255) ) )

while not dn.is_logging():
    time.sleep(0.5)
time.sleep(0.5) # Wait for drone to initialize

def mov(new_drone_coord):
    x, y, is_black = dn.mov(new_drone_coord[0], new_drone_coord[1])
    global drone_coord
    drone_coord = new_drone_coord
    return not is_black

def get_coords():
    x, y = dn.grab_x_y()
    return np.array( [x, y] )

def display_img(img):
    ax.clear()
    plt.minorticks_on()
    plt.grid(which='both', color='gray', linestyle='-', linewidth=0.2)
    ax.set_xlim(0, img.height-1)
    ax.set_ylim(0, img.width-1)
    ax.imshow(img)
    plt.pause(0.001)  # Must pause to update

def display_drone(img, vis_drone_coord):
    drone_img = img.copy()
    set_pixel(drone_img, vis_drone_coord, drone_color)
    display_img(drone_img)

def display_bad_drone(img, vis_drone_coord):
    drone_img = img.copy()
    set_pixel(drone_img, vis_drone_coord, bad_drone_color)
    display_img(drone_img)

def set_pixel(img, coords_numpy, color):
    coords_python = tuple(coords_numpy)
    img.putpixel(coords_python, color)

def get_pixel(img, coords_numpy):
    coords_python = tuple(coords_numpy)
    return img.getpixel(coords_python)

dir = np.array( [ [1, 0, 0], [0, 1, 1], [-1, 0, 2], [0, -1, 3] ] )

def size_check(coord, bg, sm):
    if coord[0] < sm:
        sm = coord[0]
    elif coord[0] > bg:
        bg = coord[0]
    if coord[1] < sm:
        sm = coord[1]
    elif coord[1] > bg:
        bg = coord[1]
    return bg, sm

def real_to_vis(real):
    vis = ( np.ceil( real * rv_mult ) + rv_off ).astype(int)
    return vis

def vis_to_real(vis):
    real = ( (vis - rv_off) / rv_mult ).astype(float)
    return real


def scan_area( ):

    global rv_mult, rv_off, vis_start, vis_img, vis_drone_coord, vis_size

    vis_starting_size = 20
    vis_increase_size = 2
    vis_border = 2
    vis_size = vis_starting_size+int(np.ceil(2*vis_border))
    vis_start_coord = 1 + int(np.ceil(vis_size / 2))
    vis_drone_coord = np.array( [ vis_start_coord, vis_start_coord ] )
   
    vis_small = vis_border
    old_small = vis_small
    vis_big = vis_size - vis_border
    old_big = vis_big    

    vis_img = Image.new('RGB', (vis_size, vis_size), unknown_color)
    vis_start = vis_drone_coord
    set_pixel(vis_img, vis_start, start_color)
    display_drone(vis_img, vis_drone_coord)

    rv_mult = np.float32( 1 / move_length )
    rv_off = ( vis_drone_coord - np.ceil( np.multiply(drone_coord, rv_mult)) ).astype(int)

    stack = np.array( [ [ vis_drone_coord[0], vis_drone_coord[1], 4 ] ] )

    while stack.shape[0] > 0:
        da_list = dir + np.array( [ stack[-1, 0 ], stack[-1, 1 ], 0 ] )
        next_coord = np.array( [] )
        for i in range(4):
            ############### Check image sizes
            specific_coord = da_list[i]
            
            vis_big, vis_small = size_check(specific_coord, vis_big, vis_small)
            if vis_big > old_big or vis_small < old_small:
                new_vis_size = int(np.ceil(vis_size * vis_increase_size))
                new_vis_img = Image.new('RGB', (new_vis_size, new_vis_size), unknown_color)
                add_to_offset = int(np.ceil( (new_vis_size - vis_size)/4 ))
                st = add_to_offset

                new_vis_img.paste(vis_img, (st, st) )

                vis_img = new_vis_img
                vis_drone_coord = vis_drone_coord + add_to_offset
                stack[:, :2] = stack[:, :2] + add_to_offset
                rv_off = rv_off + add_to_offset
                vis_size = new_vis_size
                vis_small = vis_border
                vis_big = new_vis_size - vis_border
                specific_coord[:2] = specific_coord[:2] + add_to_offset
                old_big = vis_big
                old_small = vis_small
                display_drone(vis_img, vis_drone_coord)
            ###########
            cor = get_pixel(vis_img, da_list[i, :2])
            if cor == unknown_color:
                next_coord = da_list[i]
                break
        if next_coord.size > 0:
            #test_drone_coord = drone_coord + np.multiply( dir[ np.int8(next_coord[2]), :2 ], move_length )
            #vis_test_drone_coord = real_to_vis(test_drone_coord)
            test_drone_coord = vis_to_real(next_coord[:2])
            vis_test_drone_coord = next_coord[:2]

            old_drone_coord = drone_coord
            success = mov(test_drone_coord)

            if success:
                vis_drone_coord = vis_test_drone_coord
                stack = np.append(stack, [ next_coord ], axis=0)
                use_color = line_color
                display_drone(vis_img, vis_drone_coord)
            else:
                display_bad_drone(vis_img, vis_test_drone_coord)
                #mov(old_drone_coord)
                use_color = border_color

            set_pixel(vis_img, vis_test_drone_coord, use_color)

        else:
            #back_coord = stack[-1]
            stack = np.delete(stack, -1, axis=0)
            #if stack.shape[0] > 1:
            #    match back_coord[2]:
            #        case 0:
            #            back_coord[2] = 2
            #        case 1:
            #            back_coord[2] = 3
            #        case 2:
            #            back_coord[2] = 0
            #        case 3:
            #            back_coord[2] = 1
                #test_drone_coord = drone_coord + np.multiply( dir[ np.int8(back_coord[2]), :2 ], move_length )
                #vis_drone_coord = real_to_vis(test_drone_coord)
                #test_drone_coord = vis_to_real(back_coord[:2])
                #vis_test_drone_coord = back_coord[:2]

                #success = mov(test_drone_coord)
                #if not success:
                #    print("ERROR: Drone detecting black color when this position should show white")

    ### Shrink the map
    # Get the first not unknown pixel from each side.
    # See which one has the closest and fathest coordinates.
    # Resize the map based on them with vis_border.

    vis_arr = np.array(vis_img)
    unk_arr = np.array(unknown_color)

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
            if i >= vis_size:
                break
        j = j + 1
        if j >= vis_size:
            break

    first_row = diff_coord

    diff_cor = False
    diff_coord = -1
    j = vis_size - 1
    while not diff_cor:
        i = 0
        while not diff_cor:
            if not (unk_arr == vis_arr[j, i] ).all():
                diff_cor = True
                diff_coord = j
                break
            i = i + 1
            if i >= vis_size:
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
            if i >= vis_size:
                break
        j = j + 1
        if j >= vis_size:
            break

    first_col = diff_coord

    diff_cor = False
    diff_coord = -1
    j = vis_size - 1
    while not diff_cor:
        i = 0
        while not diff_cor:
            if not (unk_arr == vis_arr[i, j] ).all():
                diff_cor = True
                diff_coord = j
                break
            i = i + 1
            if i >= vis_size:
                break
        j = j - 1
        if j < 0:
            break

    last_col = diff_coord

    first = min(first_row, first_col)
    last = max(last_row, last_col)
    vis_drone_coord = vis_drone_coord - first + vis_border
    rv_off = rv_off - first + vis_border

    first_bor = first-vis_border
    last_bor = last+vis_border

    new_vis_arr = vis_arr[first_bor:(last_bor+1), first_bor:(last_bor+1)]

    vis_img = Image.fromarray(new_vis_arr)
    vis_size = vis_img.width

    display_drone(vis_img, vis_drone_coord)

def get_dis(p1, p2):
    return int( np.sqrt( ((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2)  ) )

def create_end_point():
    line_arr = np.array(line_color)
    vis_arr = np.array(vis_img)
    max_d = 0
    point = np.array([])
    for i in range(vis_size):
        for j in range(vis_size):
            check_me = vis_arr[i, j]
            if (line_arr == check_me ).all():
                d = get_dis(vis_start, check_me)
                if d > max_d:
                    max_d = d
                    point = np.array([j, i])
    global vis_end
    vis_end = point
    print("End: ", vis_end)
    set_pixel(vis_img, vis_end, end_color)
    display_drone(vis_img, vis_drone_coord)

cake = get_coords()
mov(cake)
drone_coord = get_coords()

scan_area()
create_end_point()

print("DONE!!!")
dn.manual_exit()
time.sleep(9999)