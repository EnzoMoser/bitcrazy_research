function [image, new_segments] = vector_to_pixel(all_segments, image_size, max_line_coord, outer_radius, inner_radius, border)
%VECTOR_TO_PIXEL

% Remember: all_segments{iter}(2,:) and all_segments{iter}(end-1,:) are
% traffic points.

% New line coordinates
[~, l_s] = size(all_segments);
new_segments = cell(l_s);
for iter = 1:l_s
    new_segments{iter} = pixel_new_coords(all_segments{iter}, image_size, max_line_coord, border);
end

% Create map

image = pixel_create_map(new_segments, image_size, inner_radius, outer_radius);

end