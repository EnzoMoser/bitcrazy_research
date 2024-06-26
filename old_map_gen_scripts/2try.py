import matplotlib.pyplot as plt
import numpy as np

GRID_SIZE = 20

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
    else:
        return [[0, 0], [0, 0]]

def check_point(point, line, map):
    if point in map:
        if point not in line:
            return True
    return False

def valid_moves(cur_pos, old_pos, line, map):
    list_of_dx_dy = direction_based_turns(old_pos, cur_pos)
    if list_of_dx_dy[1] = [0, 0]:
        pass
        # Should be return
    for dx_dy in list_of_dx_dy:
        point = cur_pos + dx_dy
        print("Current pos: ", cur_pos, "\nDX_DY: ", dx_dy, "\nPoint: ", point)


def plot_line(map):
    # Initialize the line with the starting point
    line = [(0, 0)]
    current_position = (0, 0)
    visited = set()
    visited.add(current_position)
    
    while current_position != (GRID_SIZE-1, GRID_SIZE-1):
        x, y = current_position
        
        # Determine possible moves
        possible_moves = []
        if x > 0 and (x-1, y) not in visited:
            possible_moves.append((x-1, y))
        if x < GRID_SIZE-1 and (x+1, y) not in visited:
            possible_moves.append((x+1, y))
        if y > 0 and (x, y-1) not in visited:
            possible_moves.append((x, y-1))
        if y < GRID_SIZE-1 and (x, y+1) not in visited:
            possible_moves.append((x, y+1))
        
        if not possible_moves:
            break  # No valid moves left
        
        # Randomly select a move
        next_position = possible_moves[np.random.choice(len(possible_moves))]
        line.append(next_position)
        visited.add(next_position)
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
    map = np.array([[x, y] for x in range(grid_size) for y in range(grid_size)])

    line = plot_line(map)

    #display_map(map, line)

    print(line)

if __name__ == "__main__":
    main()

