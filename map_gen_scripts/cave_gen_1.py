import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

MAP_LENGTH = 100
ONE_TO_ZERO_RATIO = 1/4

def display_map(matrix):
    plt.imshow(matrix, cmap='binary_r', interpolation='nearest', vmin=0, vmax=1)
    plt.axis('off')
    plt.show()

def main():
    # Define map size
    size = MAP_LENGTH

    # Create empty map
    matrix = np.zeros((size, size))

    # Place initial 1 randomly
    x, y = np.random.randint(0, size), np.random.randint(0, size)
    matrix[x, y] = 1

    # Repeat until half or more of the map are 1's
    while np.sum(matrix) < (size ** 2) * ONE_TO_ZERO_RATIO :
        # Move to a random adjacent coordinate
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
        dx, dy = moves[random.randint(0, 7)]
        x, y = max(2, min(size - 2, x + dx)), max(2, min(size - 2, y + dy))
        
        # Place a 1 on this coordinate
        matrix[x, y] = 1

    # Display the map
    display_map(matrix)

if __name__ == "__main__":
    main()

