import matplotlib.pyplot as plt
import math
import sys
import numpy as np

GRID_SIZE = 10
LINE_FAIL_LIMIT = 1000
RELOAD_LIMIT = 100

NUM_OF_BREAK_LINES = 3

def find_crossing_points(cur_pos, old_pos):
    dx = cur_pos[0] - old_pos[0]
    dy = cur_pos[1] - old_pos[1]

    if dx > 0 and dy > 0:
        return [ (0, 1), (1, 0) ]
    elif dx < 0 and dy < 0:
        return [ (0, -1), (-1, 0) ]
    elif dx > 0 and dy < 0:
        return [ (1, 0), (0, -1) ]
    elif dx < 0 and dy > 0:
        return [ (-1, 0), (0, 1) ]
    else:
        print("AHHHHHHHHHHHHHHHHHHHHHHHH error")
        return [ (0, 1), (1, 0) ]

def direction_based_turns(old_point, new_point):
    dx = new_point[0] - old_point[0]
    dy = new_point[1] - old_point[1]
    
    if dx > 0 and dy > 0:
        return [ [1, 1], [1, 0], [0, 1] ]
    elif dx > 0 and dy == 0:
        return [ [1, 0], [1, 1], [1, -1] ]
    elif dx > 0 and dy < 0:
        return [ [1, 0], [0, -1], [1, -1] ]
    elif dx == 0 and dy > 0:
        return [ [0, 1], [1, 1], [-1, 1] ]
    elif dx == 0 and dy < 0:
        return [ [0, -1], [-1, -1], [1, -1] ]
    elif dx < 0 and dy > 0:
        return [ [-1, 1], [0, 1], [-1, 0] ]
    elif dx < 0 and dy == 0:
        return [ [-1, 0], [-1, 1], [-1, -1] ]
    elif dx < 0 and dy < 0:
        return [ [-1, -1], [-1, 0], [0, -1] ]
    elif dx == 0 and dy == 0:
        return [ [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1], [0, 1] ]
    else:
        return [ [0, 0], [0, 0] ]

def y_split(old_point, new_point) -> list:
    dx = new_point[0] - old_point[0]
    dy = new_point[1] - old_point[1]
    if dx > 0 and dy > 0:
        return [ [1, 0], [0, 1] ]
    elif dx > 0 and dy == 0:
        return [ [1, 1], [1, -1] ]
    elif dx > 0 and dy < 0:
        return [ [1, 0], [0, -1] ]
    elif dx == 0 and dy > 0:
        return [ [1, 1], [-1, 1] ]
    elif dx == 0 and dy < 0:
        return [ [-1, -1], [1, -1] ]
    elif dx < 0 and dy > 0:
        return [ [0, 1], [-1, 0] ]
    elif dx < 0 and dy == 0:
        return [ [-1, 1], [-1, -1] ]
    elif dx < 0 and dy < 0:
        return [ [-1, 0], [0, -1] ]
    else:
        return [ [0, 0], [0, 0] ]

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

def is_point_in_grid(point, grid_size):
    if point[0] >= 0:
        if point[0] < grid_size:
            if point[1] >= 0:
                if point[1] < grid_size:
                    return True
    return False

def is_point_in_line(point, line):
    if point in line:
        return True
    else:
        return False


def is_point_in_list_of_lines(point, list_of_lines):
    for line in list_of_lines:
        if point in line:
            return True
    return False

def valid_moves(cur_pos, old_pos, list_of_dx_dy, line, list_of_lines, grid_size, bad_pos_list, no_cross_list):
    possible_moves = []
    possible_merges = []
    #print("List: ", list_of_dx_dy)
    if list_of_dx_dy[0] == [0, 0]:
        return [], []
    for dx_dy in list_of_dx_dy:
        here_x, here_y = cur_pos
        go_x, go_y = dx_dy
        point = (here_x + go_x, here_y + go_y)
        #print("Current pos: ", cur_pos, "\nDX_DY: ", dx_dy, "\nPoint: ", point)
        if is_point_in_grid(point, grid_size):
            if not is_point_in_line(point, line):
                #if point not in bad_pos_list:
                if not is_point_in_list_of_lines(point, list_of_lines):
                    if abs(go_x) + abs(go_y) >= 2:
                        if point not in no_cross_list:
                            possible_moves.append(point)
                    else:
                        possible_moves.append(point)
                else:
                    possible_merges.append(point)
                #print("Point: ", point)
                #print("List of lines: ", list_of_lines)

    #print(possible_moves)
    #print("|Possible merges: ", possible_merges)
    return possible_moves, possible_merges

def create_line(cur_pos, old_pos, breaks_needed, grid_size, prev_lines, len_parent, len_prev, did_a_line_reach_end, line_fail_lim, no_cross_list):
    #print("CBreaks, needed", breaks_needed, "    Grid size: ", grid_size)
    if old_pos == cur_pos:
        line = [ cur_pos ]
        length = 0
    else:
        line = [old_pos, cur_pos]
        length = 1

    random_limit = 4/5 * grid_size

    min_len = max(3, grid_size * 3 / 20)

    break_loop = False
    break_error = False

    all_lines = []

    bad_pos_list = []

    line_fail_num = 0

    while not break_loop:
        #print("Old: ", old_pos, "    Cur: ", cur_pos, "    Length: ", length)
        if len_prev + length > random_limit:
            directioned_points = upright_biased_turns(old_pos, cur_pos)
        else:
            directioned_points = direction_based_turns(old_pos, cur_pos)

        possible_moves, possible_merges = valid_moves(cur_pos, old_pos, directioned_points, line, prev_lines, grid_size, bad_pos_list, no_cross_list)

        if did_a_line_reach_end:
            if len(possible_merges) > 0:
                if length > min_len or len_prev + length > random_limit:
                    possible_moves.extend(possible_merges)

        #print("Possible Moves: ", possible_moves)
        #print(len(possible_moves))
        if len(possible_moves) == 0:
            #print("EERORR")
            # Go back a point and remove it cur_pos from possible_moves.
            # If line length is less than or eq to 1, exit with failure, and have the line above go back one point.
            break_error = True
        else:
            if length > min_len and breaks_needed > 0:
                #print("FBreaks needed: ", breaks_needed)
                if break_loop == False:
                    #print("Break check...")
                    prev_lines_including_this = prev_lines
                    prev_lines_including_this.append(line)
                    total_len = len_prev + length
                  
                    #print("Old: ", old_pos, "     Cur: ", cur_pos)
                    y_splitting = y_split(old_pos, cur_pos)
                    pos_moves, pos_merges = valid_moves(cur_pos, old_pos, y_splitting, line, prev_lines, grid_size, bad_pos_list, no_cross_list)

                    if len(pos_moves) == 0:
                        break_error = True
                        #print("No Break")
                    elif len(pos_moves) == 1:
                        break_error = True
                        #print("No Break")
                    else:
                        #print("Breaking...")
                        new_pos_one = pos_moves[0]
                        new_pos_two = pos_moves[1]

                        #print("New pos one: ", new_pos_one, "New pos two: ", new_pos_two)

                        one_less_break = breaks_needed - 1
                        break_half = int(one_less_break/2)
                        break_floor = math.floor(break_half)
                        break_ceil = math.ceil(break_half)
                        #print("One less break: ", one_less_break, "    Half: ", break_half, "    Floor: ", break_floor, "    Ceil: ", break_ceil)
                        if one_less_break % 2 == 0:
                            # Number is even
                            break_lines_one, break_error_one, did_a_line_reach_end, temp_cross_one = create_line(new_pos_one, cur_pos, break_half, grid_size, prev_lines_including_this, length, total_len, did_a_line_reach_end, line_fail_lim, no_cross_list)
                            if not break_error_one:
                                #print("Break 2!")
                                temp_lines = prev_lines_including_this
                                temp_lines.extend(break_lines_one)
                                temp_cross_list = no_cross_list
                                temp_cross_list.extend(temp_cross_one)
                                #print("Temp: ", temp_lines)
                                #print("Cur: ", cur_pos)
                                break_lines_two, break_error_two, did_a_line_reach_end, mm = create_line(new_pos_two, cur_pos, break_half, grid_size, temp_lines, length, total_len, did_a_line_reach_end, line_fail_lim, temp_cross_list)
                        else:
                            # Number is odd
                            #print("Break is odd: ", breaks_needed - 1)
                            break_lines_one, break_error_one, did_a_line_reach_end, temp_cross_one = create_line(new_pos_one, cur_pos, break_ceil, grid_size, prev_lines_including_this, length, total_len, did_a_line_reach_end, line_fail_lim, no_cross_list)
                            if not break_error_one:
                                temp_lines = prev_lines_including_this
                                temp_lines.extend(break_lines_one)
                                temp_cross_list = no_cross_list
                                temp_cross_list.extend(temp_cross_one)
                                break_lines_two, break_error_two, did_a_line_reach_end, mm = create_line(new_pos_two, cur_pos, break_floor, grid_size, temp_lines, length, total_len, did_a_line_reach_end, line_fail_lim, temp_cross_list)
                        if (not break_error_one) and (not break_error_two):
                            breaks_needed = breaks_needed - 1
                            all_lines.extend(break_lines_one)
                            all_lines.extend(break_lines_two)
                            break_loop = True
                        #print("Done Break!")
            else:
                next_pos = possible_moves[np.random.choice(len(possible_moves))]
                #print("Next Pos: ", next_pos)
                line.append(next_pos)
                if abs(next_pos[0] - cur_pos[0]) + abs(next_pos[1] - cur_pos[1]) >= 2:
                    # Append the adjacent crossing points
                    adj_mov_one, adj_mov_two = find_crossing_points(next_pos, cur_pos)
                    pox = adj_mov_one[0] + cur_pos[0]
                    poy = adj_mov_one[1] + cur_pos[1]
                    ptx = adj_mov_two[0] + cur_pos[0]
                    pty = adj_mov_two[1] + cur_pos[1]
                    adj_point_one = (pox, poy) 
                    adj_point_two = (ptx, pty) 
                    no_cross_list.append(adj_point_one)
                    no_cross_list.append(adj_point_two)
                #if abs(next_pos[0]) - abs(next_pos[1])
                old_pos = cur_pos
                cur_pos = next_pos
                length = length + 1
                if next_pos == (grid_size-1, grid_size-1):
                    did_a_line_reach_end = True
                    break_loop = True
                if next_pos in possible_merges:
                    # Break the loop, knowing it's merged.
                    break_loop = True

        if break_error == True:
            break_error = False
            if line_fail_num > line_fail_lim or length < min_len:
                print("Error!!!!     |     Line fail num: ", line_fail_num)
                break_loop = True
                break_error = True
            else:
                print("Going back...")
                bad_pos_list.append( line[-1] ) 
                print("Line ", line)
                line.pop(-1)
                cur_pos = line[-1]
                old_pos = line[-2]
                length = length - 1

                line_fail_num = line_fail_num + 1

    all_lines.append((line))
    #print("All: ", all_lines)
    # All lines = create_line.
    return all_lines, break_error, did_a_line_reach_end, no_cross_list


def display_map(map, all_lines):
    # Plot the points and the line
    plt.scatter(map[:, 0], map[:, 1], color='blue', s=10)
    for line in all_lines:
        plt.plot(np.array(line)[:, 0], np.array(line)[:, 1], color='black', linewidth=25)
    for line in all_lines:
        plt.plot(np.array(line)[:, 0], np.array(line)[:, 1], color='white', linewidth=20)
    plt.title("Map of 20x20 Vector Points with Random Line")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.show()

def run_program(grid_size, num_of_break_lines, line_fail_limit, reload_limit):
    map = np.array([[x, y] for x in range(grid_size) for y in range(grid_size)])

    counter = 0
    all_lines, break_error, did_a_line_reach_end, no_cross_list = create_line( (0, 0), (0, 0), num_of_break_lines, grid_size, [], 0, 0, False, line_fail_limit, [] )
    while (break_error and counter < reload_limit):
        print("Failed to print good map. Trying again...")
        all_lines, break_error, did_a_line_reach_end, no_cross_list = create_line( (0, 0), (0, 0), num_of_break_lines, grid_size, [], 0, 0, False, line_fail_limit, [] )
        counter = counter + 1   

    #print(all_lines)
    if break_error:
        print("FAILED to Print Good Map after multiple attempts")
    display_map(map, all_lines)

def main():
    run_program(GRID_SIZE, NUM_OF_BREAK_LINES, LINE_FAIL_LIMIT, RELOAD_LIMIT)

if __name__ == "__main__":
    main()

