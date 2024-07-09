%% Follow path

% Define start and end coordinates
start_point = m_line(1,:);
end_point = m_line(end,:);

% Adjust to corresponding pixel coords
start_point = pixel_new_coords(start_point, image_size, real_grid_size, border);
end_point = pixel_new_coords(end_point, image_size, real_grid_size, border);

% Adjust the pixel coords to the drone's visual pixel 
vis_start_point = real_to_vis_coord(start_point, offset_plus, offset_mult);
vis_end_point = real_to_vis_coord(end_point, offset_plus, offset_mult);

vis_drone_coord = vis_start_point; % Inside the drone's visual map
drone_coord = start_point;         % The pseudo "real" map

pseudo_fig = 3; % Display "Real" on Figure 3
vis_fig = 4;    % Display visual on Figure 4

% Find the path
path = bfs_path(vis_img, vis_start_point, vis_end_point, walkable_colors);

% Display the path
disp('Path:');
disp(path);

time_delay = 0.01;
% Use the path
drone_follow_coords(vis_img, img, path, drone_coord, drone_radius, move_length, drone_color, bad_drone_color, time_delay, offset_plus, offset_mult, walkable_colors, ...
    pseudo_fig, vis_fig);