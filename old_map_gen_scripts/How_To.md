# How To

Start the line based on given coordinates, old coordinate, how often it needs to break, grid_size, parent_lines.
Parent_line is empty. Big whoop.

When the line is 1/3 of grid_size and is above the number 3, it breaks into two, creating Y crossroads.

The number of remaining breakages needed is spread across the two new lines.
Append the line to a parent_lines list, to give to the break lines.

## Break lines
These lines are given a new starting coordinate, old coordinate, how often it needs to break, grid_size, parent_lines.
Get parent_line_length from the latest parent_line.

When line is 1/3 of parent_line_length and is above the number 3, break.

Append this line to parent_lines.
Split the remaining breakages needed amongst the other lines.

This repeats until there are no more breakages. Then, the lines move with a bias to top right.

If the total line length of all the parent lines is ever 3/4 of the grid_size:
    Stop breaking lines, and start biasing towards the top right. 

If the lines hit a wall or ceiling, continue to top right.



If there are no points on a line,
If a line will attempt to be made 100 times. If it fails 100 times, it will tell the parent line that it failed. The parent line will then try 100 times.

A line cannot merge into another line if it is not long enough, or if no line has yet to reach the end.
