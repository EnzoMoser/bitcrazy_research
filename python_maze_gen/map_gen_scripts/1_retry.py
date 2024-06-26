import matplotlib.pyplot as plt
import math
import sys
import numpy as np

GRID_SIZE = 10
MAIN_LINE_FAIL_LIMIT = 9000
BREAK_LINE_FAIL_LIMIT = 9000

MAX_FAIL_LIMIT = 9000

NUM_OF_BREAK_LINES = 2

def find_crossing_points(cur_pos, old_pos):
    dx = cur_pos[0] - old_pos[0]
    dy = cur_pos[1] - old_pos[1]

    if dx == 1 and dy == 1:
        return [ (0, 1), (1, 0) ]
    elif dx == -1 and dy == -1:
        return [ (0, -1), (-1, 0) ]
    elif dx == 1 and dy == -1:
        return [ (1, 0), (0, -1) ]
    elif dx == -1 and dy == 1:
        return [ (-1, 0), (0, 1) ]
    else:
        print("AHHHHHHHHHHHHHHHHHHHHHHHH error")
        return [ (0, 1), (1, 0) ]

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

def valid_moves(cur_pos, old_pos, list_of_dx_dy, all_lines, grid_size, no_cross_list):
    possible_moves = []
    if list_of_dx_dy[0] == [0, 0]:
        pass
        # Should be return
    for dx_dy in list_of_dx_dy:
        here_x, here_y = cur_pos
        go_x, go_y = dx_dy
        point = (here_x + go_x, here_y + go_y)
        #print("Current pos: ", cur_pos, "\nDX_DY: ", dx_dy, "\nPoint: ", point)

        if abs(go_x) + abs(go_y) >= 2:
            if point in no_cross_list:
                return []

        is_available = True
        for line in all_lines:
            if not point_available(point, line, grid_size):
                is_available = False
                break
        if is_available:
            possible_moves.append(point)
    return possible_moves

def create_line(grid_size, no_cross_list, all_lines):
    # Initialize the line with the starting point
    line = [(0, 0)]
    current_position = (0, 0)
    counter = 0
    old_position = current_position
    test_line = all_lines
    test_line.append(line)

    while counter <= grid_size * 1 / 2:
        counter = counter + 1
        directioned_points = direction_based_turns(old_position, current_position)
        test_line[-1] = line
        possible_moves = valid_moves(current_position, old_position, directioned_points, test_line, grid_size, no_cross_list)
        # Randomly select a move
        if len(possible_moves) == 0:
            return [], []
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)
        if abs(next_position[0] - current_position[0]) + abs(next_position[1] - current_position[1]) >= 2:
            # Append the adjacent crossing points
            adj_mov_one, adj_mov_two = find_crossing_points(next_position, current_position)
            pox = adj_mov_one[0] + current_position[0]
            poy = adj_mov_one[1] + current_position[1]
            ptx = adj_mov_two[0] + current_position[0]
            pty = adj_mov_two[1] + current_position[1]
            adj_point_one = (pox, poy) 
            adj_point_two = (ptx, pty) 
            no_cross_list.append(adj_point_one)
            no_cross_list.append(adj_point_two)
        old_position = current_position
        current_position = next_position
   
    while current_position != (grid_size-1, grid_size-1):
        directioned_points = upright_biased_turns(old_position, current_position)
        test_line[-1] = line
        possible_moves = valid_moves(current_position, old_position, directioned_points, test_line, grid_size, no_cross_list)
        # Randomly select a move
        if len(possible_moves) == 0:
            return [], []
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)

        if abs(next_position[0] - current_position[0]) + abs(next_position[1] - current_position[1]) >= 2:
            # Append the adjacent crossing points
            adj_mov_one, adj_mov_two = find_crossing_points(next_position, current_position)
            pox = adj_mov_one[0] + current_position[0]
            poy = adj_mov_one[1] + current_position[1]
            ptx = adj_mov_two[0] + current_position[0]
            pty = adj_mov_two[1] + current_position[1]
            adj_point_one = (pox, poy) 
            adj_point_two = (ptx, pty) 
            no_cross_list.append(adj_point_one)
            no_cross_list.append(adj_point_two)

        old_position = current_position
        current_position = next_position

    return line, no_cross_list

def display_map(map, all_lines):
    # Plot the points and the line
    plt.scatter(map[:, 0], map[:, 1], color='blue', s=10)
    for line in all_lines:
        plt.plot(np.array(line)[:, 0], np.array(line)[:, 1], color='black', linewidth=35)
    for line in all_lines:
        plt.plot(np.array(line)[:, 0], np.array(line)[:, 1], color='white', linewidth=20)
    plt.title("Map of 20x20 Vector Points with Random Line")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.show()


def compare_lines(break_line, all_lines, grid_size, minimum_length):
    length = len(break_line)
    halfway = math.ceil(length / 2) - 1
    bot = 0
    top = 0
    i = halfway
    while i < length - 1:
        for main_line in all_lines:
            if break_line[i] in main_line:
                #print("YES")
                break
        else:
            #print("no")
            i = i + 1
            continue
        top = i
        #print("I is ", i)
        break

    i = halfway
    while i > 0:
        for main_line in all_lines:
            if break_line[i] in main_line:
                break
        else:
            i = i - 1
            continue
        bot = i
        break

    if bot == 0 or top == 0:
        return []

    connect_line = break_line
    i = length - 1
    while i > top:
        connect_line.pop(-1)
        i = i - 1
    i = 0
    while i < bot:
        connect_line.pop(0)
        i = i + 1
    if len(connect_line) < minimum_length:
        return []
    return connect_line

def is_diag(point_a, point_b):
    if abs( point_a[0] - point_b[0] ) + abs( point_a[1] - point_b[1] ) == 2:
        return True
    else:
        return False


def point_in_list(point)

def line_no_crosses(line, other_lines):
    length = len(line)
    i = 0

    while i < length - 1:
        if is_diag(line[i+1], line[i]):
            adj_a, adj_b = find_crossing_points(line[i+1], line[i])
            point_a = line[i]
            point_b = line[i]
            
            print("Adj A: ", adj_a, "   Adj_B: ", adj_b)

            point_a = ( point_a[0] + adj_a[0], point_a[1] + adj_a[1] )
            point_b = ( point_b[0] + adj_b[0], point_b[1] + adj_b[1] )
           
            print("PA: ", point_a, "PB: ", point_b)

            if point_a in line:
                return False
            if point_b in line:
                return False
            
            for bline in other_lines:
                if point_a in bline:
                    return False
                if point_b in bline:
                    return False
        i = i + 1
    return True

def main():
    grid_size = GRID_SIZE
    main_line_fail_limit = MAIN_LINE_FAIL_LIMIT 
    break_line_fail_limit = BREAK_LINE_FAIL_LIMIT 
    num_of_break_lines = NUM_OF_BREAK_LINES

    map = np.array([[x, y] for x in range(grid_size) for y in range(grid_size)])
   
    line = []
    counter = 0

    while line == []:
        counter = counter + 1
        print("Tried '", counter, "' times...")
        line, no_cross_list = create_line(grid_size, [], [])
        if counter > main_line_fail_limit:
            sys.exit("Failed to produce line")
    all_lines = []
    all_lines.append(line)

    while num_of_break_lines > 0:
        break_line = []
        counter = 0
        while break_line == [] or connect_line == []:
            counter = counter + 1
            print("Trying ", counter, "times.")
            break_line, break_cross_list = create_line(grid_size, [], [])
            if counter > main_line_fail_limit:
                sys.exit("Failed to produce linesss")
            if break_line != []:
                connect_line = compare_lines(break_line, all_lines, grid_size, 3)
                if connect_line != []:
                    if line_no_crosses(connect_line, all_lines) == False:
                        connect_line == []
        num_of_break_lines = num_of_break_lines - 1
        all_lines.append(connect_line)

    display_map(map, all_lines)

if __name__ == "__main__":
    main()

