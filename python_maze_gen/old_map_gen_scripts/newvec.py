import matplotlib.pyplot as plt
import numpy as np

def generate_line(points):
    line = [np.random.choice(len(points))]  # Start with a random point
    while len(line) <= 10:
        # Get the last point in the line
        last_point = points[line[-1]]

        # Find adjacent points
        adjacent_points = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                adjacent_point = [last_point[0] + dx, last_point[1] + dy]
                idx = np.where((points == adjacent_point).all(axis=1))[0]
                for point in idx:
                    if point in line:
                        continue
                    #elif: 
                    #    continue
                    else:
                        adjacent_points.append(adjacent_point)

        # Choose a random adjacent point
        if len(adjacent_points) > 0:
            next_point = np.random.choice(len(adjacent_points))
            line.append(np.where((points == adjacent_points[next_point]).all(axis=1))[0][0])
        else:
            break

    return np.array([points[i] for i in line])

def main():
    # Create a 20x20 grid of points
    grid_size = 20
    points = np.array([[x, y] for x in range(grid_size) for y in range(grid_size)])

    line = generate_line(points)

    # Plot the points and the line
    plt.scatter(points[:, 0], points[:, 1], color='blue', s=10)
    plt.plot(line[:, 0], line[:, 1], color='black', linewidth=25)
    plt.plot(line[:, 0], line[:, 1], color='white', linewidth=20)
    plt.title("Map of 20x20 Vector Points with Random Line")
    plt.xlabel("X-coordinate")
    plt.ylabel("Y-coordinate")
    plt.grid(True)
    plt.show()

    print(line)

if __name__ == "__main__":
    main()

