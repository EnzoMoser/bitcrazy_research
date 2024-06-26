import matplotlib.pyplot as plt
import math
import sys
import numpy as np

GRID_SIZE = 100
MAIN_LINE_FAIL_LIMIT = 1000
BREAK_LINE_FAIL_LIMIT = 1000

MAX_FAIL_LIMIT = 5000

NUM_OF_BREAK_LINES = 9

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

def valid_moves(cur_pos, old_pos, list_of_dx_dy, all_lines, grid_size):
    possible_moves = []
    if list_of_dx_dy[0] == [0, 0]:
        pass
        # Should be return
    for dx_dy in list_of_dx_dy:
        here_x, here_y = cur_pos
        go_x, go_y = dx_dy
        point = (here_x + go_x, here_y + go_y)
        #print("Current pos: ", cur_pos, "\nDX_DY: ", dx_dy, "\nPoint: ", point)
        is_available = True
        for line in all_lines:
            if not point_available(point, line, grid_size):
                is_available = False
                break
        if is_available:
            possible_moves.append(point)
    return possible_moves

def create_line(grid_size):
    # Initialize the line with the starting point
    line = [(0, 0)]
    current_position = (0, 0)
    counter = 0
    old_position = current_position
    all_lines = []
    all_lines.append(line)

    while counter <= grid_size * 2 / 3:
        counter = counter + 1
        directioned_points = direction_based_turns(old_position, current_position)
        possible_moves = valid_moves(current_position, old_position, directioned_points, all_lines, grid_size)
        # Randomly select a move
        if len(possible_moves) == 0:
            return []
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)
        old_position = current_position
        current_position = next_position
        all_lines[0] = line
   
    while current_position != (grid_size-1, grid_size-1):
        directioned_points = upright_biased_turns(old_position, current_position)
        possible_moves = valid_moves(current_position, old_position, directioned_points, all_lines, grid_size)
        # Randomly select a move
        if len(possible_moves) == 0:
            return []
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)
        old_position = current_position
        current_position = next_position
        all_lines[0] = line

    return np.array(line)

def create_break_line(all_lines, line_num, grid_size):
    main_line = all_lines[line_num]
    main_line_length = len(main_line)
    print("Main Line length ", main_line_length)
    starting_num = math.floor(main_line_length * 1/3)
    print("Starting num ", starting_num)
    if starting_num <= 0:
        print("BIG ERROR")
        # Add an Error handler here
        pass
    # Initialize the line with the starting at the line.
    line = [main_line[starting_num]]
    current_position = main_line[starting_num]
    counter = 0
    old_position = current_position

    while counter <= main_line_length * 2 / 3:
        counter = counter + 1
        directioned_points = direction_based_turns(old_position, current_position)
        possible_moves = valid_moves(current_position, old_position, directioned_points, all_lines, grid_size)
        # Randomly select a move
        if len(possible_moves) == 0:
            return np.array(line)
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)
        old_position = current_position
        current_position = next_position
        all_lines[0] = line

    while current_position != (grid_size-1, grid_size-1):
        directioned_points = upright_biased_turns(old_position, current_position)
        possible_moves = valid_moves(current_position, old_position, directioned_points, all_lines, grid_size)
        # Randomly select a move
        if len(possible_moves) == 0:
            return np.array(line)
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)
        old_position = current_position
        current_position = next_position
        all_lines[0] = line

    return np.array(line)

def display_map(map, all_lines):
    # Plot the points and the line
    plt.scatter(map[:, 0], map[:, 1], color='blue', s=10)
    for line in all_lines:
        plt.plot(line[:, 0], line[:, 1], color='black', linewidth=25)
    for line in all_lines:
        plt.plot(line[:, 0], line[:, 1], color='white', linewidth=20)
    plt.title("Map of 20x20 Vector Points with Random Line")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.show()

def main():
    grid_size = GRID_SIZE
    main_line_fail_limit = MAIN_LINE_FAIL_LIMIT 
    break_line_fail_limit = BREAK_LINE_FAIL_LIMIT 
    num_of_break_lines = NUM_OF_BREAK_LINES

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
            if counter > main_line_fail_limit:
                sys.exit("Failed to produce line")

    all_lines = []

    all_lines.append(line)

    for i in range(num_of_break_lines):
        print(i)
        break_line = create_break_line(all_lines, i, grid_size)
        if not hasattr(line, 'all'):
            print("Failed the generate break_line, trying again...")
            counter = 1
            break_line = create_break_line(all_lines, i, grid_size)
            while not hasattr(line, 'all'):
                counter = counter + 1
                print("Tried '", counter, "' times...")
                break_line = create_break_line(all_lines, i, grid_size)
                if counter > break_line_fail_limit:
                    sys.exit("Failed to produce break_line")
        all_lines.append(break_line)

    display_map(map, all_lines)

if __name__ == "__main__":
    main()

