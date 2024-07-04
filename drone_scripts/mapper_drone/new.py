from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# Load the image using PIL
image_path = 'vis_img.png'
image = Image.open(image_path)

vis_img = image
vis_size = vis_img.width

border_color = (0, 0, 0)
line_color = (255, 255, 255)
unknown_color = (130, 130, 200)
start_color = (0, 255, 255)
end_color = (255, 255, 0)

bad = { unknown_color, border_color }

vis_start = np.array([6, 4])
vis_end = np.array([7, 3])

def get_dis(p1, p2):
    return int( np.sqrt( ((p1[0]-p2[0])**2) + ((p1[1]-p2[1])**2)  ) )

def set_pixel(img, coords_numpy, color):
    coords_python = tuple(coords_numpy)
    img.putpixel(coords_python, color)

def create_end_point():
    line_arr = np.array(line_color)
    vis_arr = np.array(vis_img)
    max_d = 0
    point = np.array([])
    for i in range(vis_size):
        for j in range(vis_size):
            check_me = vis_arr[i, j]
            if (line_arr == check_me ).all():
                d = get_dis(vis_start, np.array( [j, i] ))
                if d > max_d:
                    max_d = d
                    point = np.array([j, i])
    global vis_end
    vis_end = point
    if vis_end.size <= 0:
        print("No End point!")
    else:
        print("End: ", vis_end)
        set_pixel(vis_img, vis_end, end_color)


from collections import deque
import numpy as np
from PIL import Image

def bfs_path(img, start_coord, end_coord, bad_c):
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
                if neighbor_tuple not in visited:
                    pix = img.getpixel((neighbor[0], neighbor[1]))
                    nop = False
                    for cor in bad_c:
                        if pix == cor:
                            nop = True
                            break
                    if not nop:
                        queue.append(neighbor)
                        visited.add(neighbor_tuple)
                        came_from[neighbor_tuple] = tuple(current)
    
    # Return None if no path is found
    return None

#create_end_point()

def find_first_instance(img, color):
    arr = np.array(img)
    for y in range(img.height):
        for x in range(img.width):
            if (arr[y, x] == color).all():  # RGB value for white
                return np.array( [x, y] )
    
    # If no white pixel is found
    return None

drone_coord = (0, 0)
move_length = 2

vis_start = find_first_instance(vis_img, start_color)
vis_end = find_first_instance(vis_img, end_color)
vis_drone_coord = vis_start
vis_img = Image.open('vis_img.png')
vis_size = vis_img.width
rv_mult = np.float32( 1 / move_length )
rv_off = ( vis_drone_coord - np.ceil( np.multiply(drone_coord, rv_mult)) ).astype(int)

print(vis_start)
print(vis_end)

# Setup the matplotlib figure and axis
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

ax.clear()
plt.minorticks_on()
plt.grid(which='both', color='gray', linestyle='-', linewidth=0.2)
ax.set_xlim(0, vis_img.height-1)
ax.set_ylim(0, vis_img.width-1)
ax.imshow(vis_img)
plt.pause(9999)  # Must pause to update