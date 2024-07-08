# Mapper Drone
Make sure to read the script to understand how it works before running. You might need to adjust the shutter speed tolerances in control_real_drone.py depending on the light level of your area.

The main script to run is "main.py"

The drone must be equipped with the Flow Deck motion sensor, and any deck that provides an absolute positioning system.

Delete "vis_img.png" when mapping out a new area for the drone to pathfind in.

If the script does NOT find "vis_img.png", it will map the area, and then save this area as "vis_img.png" before stopping. Both a start and end point is marked. The start point is wherever the drone starts. The end point is furthest crossable distance to the start point (It does not care about uncrossable area).

If the script does find "vis_img.png", it will assume the drone is placed at the start point of the area, and will create a path based on the map from the image in order to reach the end point. If it detects new uncrossable area, it will mark it as a temporary obstacle and will recalculate a new path. If after successfully moving between points, it finds more uncrossable area, it will wipe the map of previous obstacles before marking the new ones. 

Ideas to expand upon:

- The main script was written with the intention of allowing one to replace "control_real_drone.py" with a fake simulation. This allows for running scripts without needing the real physical setup, as it can become quite tedious.

- Cruise control for the drones. The largest limitation here would be not having enough sensors. Sensors for detecting obstacles on the sides, such as other drones, would be recommended.

- A way to display a newly generated area for the drones to map and follow. This could also automate the process of placing random temporary obstacles and roadblocks along the map.
