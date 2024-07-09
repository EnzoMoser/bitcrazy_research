%% Scan area
drone_radius = 2; % Make sure the drone radius is smaller than the inner line radius.
drone_coord = new_segments{1}(1,:); % Start at the start of the first line segment.

drone_color = [0 255 0];
bad_drone_color = [255 0 255]; % Color of the drone if it is inside a border.

move_length = 2; % In the pseudo "real" map, the drone will take "move_length" steps.
% In the drone's visual map, it will take 1 step.

time_delay = 0; % Set to 0 for instant scanning.
% Otherwise, set to 0.01 to watch it in realtime.

walkable_colors = [255 255 255; 0 255 0]; % The default let's the drone move
% on white or green.

border_color = [0, 0, 0]; % The drone will avoid touching this color.
line_color = [255, 255, 255]; % The drone will move on this color.
unknown_color = [80, 80, 180]; % The drone will try to move to this color
% and change it to "line_color" or "border_color".

start_location_color = [0 255 255]; % The color of where the drone starts
current_location_color = [255 255 0]; % Where the drone currently is

vis_border = 1; % If the drone reaches the border in the its visual head map,
% it will increase the image size.

vis_starting_size = 4; % Starting image size.
vis_increase_size = 2; % Scale to increase size.
% The drone will cut the image size after scanning. Set time_delay above 0
% to see the drone mapping the area in realtime.

real_fig = 3;
vis_fig = 4;

% Function to scan the area.
[ vis_img, vis_drone_coord, offset_plus, offset_mult, drone_coord ] = scan_area(img, drone_coord, drone_radius, ...
    time_delay, move_length, walkable_colors, drone_color, ...
    bad_drone_color, line_color, border_color, vis_border, ...
    vis_starting_size, vis_increase_size, unknown_color, ...
    current_location_color, real_fig, vis_fig);

% Display visual map from drone's perspective
pixel_display_image(set_pixel_color(vis_img, vis_drone_coord, current_location_color), vis_fig);

% Display the "real" map of where the drone "really" is
new_image = pixel_draw_circle(img, drone_coord, drone_radius, drone_color);
pixel_display_image(new_image, real_fig);