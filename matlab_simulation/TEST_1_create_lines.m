%% ---- Step 1 ---- Create the vector map

% rng(0,'twister'); % Fix the RNG

grid_size = 10;   % Size of grid lines can move in
num_branches = 3; % Number of branched lines. To avoid very long wait times, they might branch more or less often.

% Have a read of the file "create_lines.m" for more information. There are
% additional parameters that can be adjusted.
[m_line, b_lines, traffic_lights] = create_lines(grid_size, num_branches, [], [], [] );

% Segment the main line and branched lines based on the traffic lights.
segments = segment_lines(m_line, b_lines, traffic_lights);

% The real grid size. This allows for traffic lights in-between line
% segments.
real_grid_size = grid_size * 2;

% Display the vector lines with their traffic points on a graph.
vector_display_lines(segments, real_grid_size, 1);

%% ---- Step 2 ---- Pixelize vector map
% Create the pixel version
image_size = 200;   % Image pixel width
inner_radius = 3;   % Size of the white lines
outer_radius = 8;   % Size of the black lines underneath the white lines
border = 10;        % Simple border. Reduces usable pixel width in image for lines.

[img, new_segments] = vector_to_pixel(segments, image_size, real_grid_size, outer_radius, inner_radius, border);

% Display the pixelized lines.
pixel_display_image(img,3)