import matplotlib.pyplot as plt
import sys
import numpy as np

GRID_SIZE = 20
MAX_LINE_FAIL_LIMIT = 1000

def direction_based_turns(old_point, new_point):
    dx = new_point[0] - old_point[0]
    dy = new_point[1] - old_point[1]
    
    if dx > 0 and dy > 0:
        return [[1, 1], [1, 0], [0, 1]]
    elif dx > 0 and dy == 0:
        return [[1, 0], [1, 1], [1, -1]]
    elif dx > 0 and dy < 0:
        return [[1, 0], [0, -1], [1, -1]]
    elif dx == 0 and dy > 0:
        return [[0, 1], [1, 1], [-1, 1]]
    elif dx == 0 and dy < 0:
        return [[0, -1], [-1, -1], [1, -1]]
    elif dx < 0 and dy > 0:
        return [[-1, 1], [0, 1], [-1, 0]]
    elif dx < 0 and dy == 0:
        return [[-1, 0], [-1, 1], [-1, -1]]
    elif dx < 0 and dy < 0:
        return [[-1, -1], [-1, 0], [0, -1]]
    elif dx == 0 and dy == 0:
        return [[1, 0], [0, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1] ]
    else:
        return [[0, 0], [0, 0]]

def upright_biased_turns(old_point, new_point):
    dx = new_point[0] - old_point[0]
    dy = new_point[1] - old_point[1]
    
    if dx > 0 and dy > 0:
        return [[1, 1], [1, 0], [0, 1]]
    elif dx > 0 and dy == 0:
        return [[1, 0], [1, 1]]
    elif dx > 0 and dy < 0:
        return [[1, 0]]
    elif dx == 0 and dy > 0:
        return [[0, 1], [1, 1]]
    elif dx == 0 and dy < 0:
        return [[1, -1]]
    elif dx < 0 and dy > 0:
        return [[0, 1]]
    elif dx < 0 and dy == 0:
        return [[-1, -1]]
    elif dx < 0 and dy < 0:
        return [[0, -1]]
    else:
        return [[0, 0], [0, 0]]

def point_available(point, line, grid_size):
    if point[0] >= 0:
        if point[0] < grid_size:
            if point[1] >= 0:
                if point[1] < grid_size:
                    if point not in line:
                        return True
    return False

def valid_moves(cur_pos, old_pos, list_of_dx_dy, line, grid_size):
    possible_moves = []
    if list_of_dx_dy[0] == [0, 0]:
        pass
        # Should be return
    for dx_dy in list_of_dx_dy:
        here_x, here_y = cur_pos
        go_x, go_y = dx_dy
        point = (here_x + go_x, here_y + go_y)
        #print("Current pos: ", cur_pos, "\nDX_DY: ", dx_dy, "\nPoint: ", point)
        if point_available(point, line, grid_size):
            possible_moves.append(point)
    return possible_moves

def create_line(grid_size):
    # Initialize the line with the starting point
    line = [(0, 0)]
    current_position = (0, 0)
    counter = 0
    old_position = current_position

    while counter <= 10:
        counter = counter + 1
        directioned_points = direction_based_turns(old_position, current_position)
        possible_moves = valid_moves(current_position, old_position, directioned_points, line, grid_size)
        # Randomly select a move
        if len(possible_moves) == 0:
            return []
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)
        old_position = current_position
        current_position = next_position
   
    while current_position != (grid_size-1, grid_size-1):
        directioned_points = upright_biased_turns(old_position, current_position)
        possible_moves = valid_moves(current_position, old_position, directioned_points, line, grid_size)
        # Randomly select a move
        if len(possible_moves) == 0:
            return []
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)
        old_position = current_position
        current_position = next_position

    return np.array(line)

def display_map(map, line):
    # Plot the points and the line
    plt.scatter(map[:, 0], map[:, 1], color='blue', s=10)
    plt.plot(line[:, 0], line[:, 1], color='black', linewidth=25)
    plt.plot(line[:, 0], line[:, 1], color='white', linewidth=20)
    plt.title("Map of 20x20 Vector Points with Random Line")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.show()

def main():
    grid_size = GRID_SIZE
    max_line_fail_limit = MAX_LINE_FAIL_LIMIT 
    
    map = np.array([[x, y] for x in range(grid_size) for y in range(grid_size)])
    
    line = create_line(grid_size)
    if not hasattr(line, 'all'):
        print("Failed the generate line, trying again...")
        counter = 1
        line = create_line(grid_size)
        while not hasattr(line, 'all'):
            counter = counter + 1
            print("Tried '", counter, "' times...")
            line = create_line(grid_size)
            if counter > max_line_fail_limit:
                sys.exit("Failed to produce line")

    display_map(map, line)

    print(line)

if __name__ == "__main__":
    main()

