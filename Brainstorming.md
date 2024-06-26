# Brainstorm

## First,
Generate a main line.
The line is random for half the grid_size.
Then, the line makes turns that only go up, right or upright.
If the line hits a wall or ceiling, it will continue in one direction until it hits the end (grid_size x grid_size)

## Then,
Define the total number of breakaway lines you want as a global variable.
Check if the grid_size and line length are long enough to accomodate this. Otherwise, go smaller.

Have a range to randomly pick where to start the first break-off line.
This break-off line can break a second-time if three or more break-off lines wanted.

Lines should break by a 90 degree angle from the main line.
Make sure the line break is in a Y shape

### Breakaway line #1
This line will break from the main line when it is 1/3 of the way to the end.
The line will go in a valid turn based on the line direction.
The line will then move to be perpendicular from this direction.
After a set length, it will move towards the right, upright, or up towards the end goal.

### Breakaway line #2
This line will break from the main line when it is 2/3 of the way to the end.

### Breakaway line #3
This line will break from breakaway line #1 when it is 1/3 of the way there.

### Break #4
from line 2

### break #5
from line 3

etc. etc.


1. Make the line reach the end randomly
