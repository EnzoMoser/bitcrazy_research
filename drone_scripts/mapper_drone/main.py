import control_real_drone as dn
import sys
import time
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt

move_length = np.float16(0.08) # Move length in meters

# Setup the matplotlib figure and axis
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()
plt.axis('off')  # Turn off axis
ax.imshow(Image.new('RGB', (20, 20), (255, 255, 255) ) )

while not dn.is_logging():
    time.sleep(0.5)

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
    ax.imshow(img)
    plt.pause(0.001)  # Must pause to update

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

def scan_area( ):
    border_color = (0, 0, 0)
    line_color = (255, 255, 255)
    unknown_color = (130, 130, 200)
    drone_color = (160, 0, 180)
    
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
    print(drone_coord)
    real_big = max( drone_coord[0], drone_coord[1]  )
    print(real_big)
    real_small = min( drone_coord[0], drone_coord[1]  )
    print(real_small)

    vis_img = Image.new('RGB', (vis_size, vis_size), unknown_color)
    set_pixel(vis_img, vis_drone_coord, line_color)
    drone_img = vis_img.copy()
    set_pixel(drone_img, vis_drone_coord, drone_color)
    display_img(drone_img)

    rv_mult = np.float32( 1 / move_length )
    rv_off = ( vis_drone_coord - np.ceil( np.multiply(drone_coord, rv_mult)) ).astype(int)

    stack = np.array( [ [ vis_drone_coord[0], vis_drone_coord[1], 4 ] ] )

    while True:
        da_list = dir + np.array( [ stack[-1, 0 ], stack[-1, 1 ], 0 ] )
        next_coord = np.array( [] )
        for i in range(4):
            ############### Check image sizes
            specific_coord = da_list[i]
            
            vis_big, vis_small = size_check(specific_coord, vis_big, vis_small)
            if vis_big > old_big or vis_small < old_small:
                display_img(vis_img)
                time.sleep(1)
                drone_img = vis_img.copy()
                set_pixel(drone_img, vis_drone_coord, drone_color)
                display_img(drone_img)
                time.sleep(1)
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
                display_img(vis_img)
                time.sleep(1)
                drone_img = vis_img.copy()
                set_pixel(drone_img, vis_drone_coord, drone_color)
                display_img(drone_img)
                time.sleep(1)
            ###########
            cor = get_pixel(vis_img, da_list[i, :2])
            if cor == unknown_color:
                next_coord = da_list[i]
                break
        if next_coord.size > 0:
            test_drone_coord = drone_coord + np.multiply( dir[ np.int8(next_coord[2]), :2 ], move_length )
            vis_test_drone_coord = ( np.ceil( test_drone_coord * rv_mult ) + rv_off ).astype(int)

            old_drone_coord = drone_coord
            success = mov(test_drone_coord) 
            real_big, real_small = size_check(drone_coord, real_big, real_small)

            if success:
                vis_drone_coord = vis_test_drone_coord
                stack = np.append(stack, [ next_coord ], axis=0)
                use_color = line_color
            else:
                mov(old_drone_coord)
                use_color = border_color
            set_pixel(vis_img, vis_test_drone_coord, use_color)
        else:
            back_coord = stack[-1]
            stack = np.delete(stack, -1, axis=0)
            match back_coord[2]:
                case 0:
                    back_coord[2] = 2
                case 1:
                    back_coord[2] = 3
                case 2:
                    back_coord[2] = 0
                case 3:
                    back_coord[2] = 1
            test_drone_coord = drone_coord + np.multiply( dir[ np.int8(back_coord[2]), :2 ], move_length )
            vis_drone_coord = ( np.ceil( test_drone_coord * rv_mult ) + rv_off ).astype(int)
            success = mov(test_drone_coord)
            if not success:
                print("EERORRR")
        drone_img = vis_img.copy()
        set_pixel(drone_img, vis_drone_coord, drone_color)
        display_img(drone_img)
        if stack.shape[0] <= 1:
            break

    ### Shrink the map
    # Get the first not unknown pixel from each side.
    # See which one has the closest and fathest coordinates.
    # Resize the map based on them with vis_border.

cake = get_coords()
mov(cake)
drone_coord = get_coords()
scan_area()

print("DONE!!!")
dn.manual_exit()
time.sleep(9999)
