%% ---- Step 1 ---- Find all line paths
start_point = m_line(1,:); % The start of the main line
end_point = m_line(end,:); % The end of the main line

% Create a table of all possible paths you could take to get from
% start_point to end_point. 
truth_table = traffic_truth_table(segments, start_point, end_point);

% To simulate random traffic lights, one can:
% - Choose a random array from the list "truth_table"
% - Open and close the line segments based on this table.
% - Open an additional random amount of random line segments

% This ensures that at least one path is always viable, while still
% simulating traffic lights.

%% ---- Step 2 ---- Cycle through traffic points.

repeat_n_times = 10; % How often to repeat the line path options before stopping.

% Although this function blocks off and allows lines using colored circles at the
% start and end of a line segment, one could rewrite it to color the entire line segment
% instead. You can also color the lines white instead of green and black instead of red.

[~, ff] = size(truth_table);
for loop_for_n_times = 1:repeat_n_times
    for iter = 1:ff
        % Display next path.
        him = traffic_light_cycler(img, new_segments, truth_table, iter, inner_radius, 'green', 'red');
        pixel_display_image(him,2)
        pause(1)
    end
end