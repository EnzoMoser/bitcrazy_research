from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import random
import time

def random_color():
    """Generate a random color."""
    return tuple(random.randint(0, 255) for _ in range(3))

# Create a 200x200 black image
image = Image.new('RGB', (200, 200), color='black')
line_position = 100  # middle of the 200x200 image

# Setup the matplotlib figure and axis
plt.ion()  # Turn on interactive mode
fig, ax = plt.subplots()

try:
    while True:
        # Create a new drawing object
        draw = ImageDraw.Draw(image)

        # Draw a vertical line down the middle with a random color
        color = random_color()
        draw.line((line_position, 0, line_position, 200), fill=color)

        # Display the image
        ax.clear()  # Clear the previous image
        ax.imshow(image)
        plt.axis('off')  # Turn off axis
        plt.draw()  # Draw the updated image
        plt.pause(1)  # Pause for 1 second

        # Clear the previous drawing by resetting the image
        image = Image.new('RGB', (200, 200), color='black')

except KeyboardInterrupt:
    # Handle the user manually stopping the loop
    print("Animation stopped.")

