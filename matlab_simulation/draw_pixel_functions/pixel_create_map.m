function image = pixel_create_map(list_lines, image_size, inner_radius, outer_radius)

image = zeros(image_size, image_size, 'uint8');
image(:, :, 1) = 80;
image(:, :, 2) = 80;
image(:, :, 3) = 180;


[~, length_lines] = size(list_lines);

for iter = 1:length_lines
    image = pixel_draw_line(image, 'black', list_lines{iter}, outer_radius);
end
for iter = 1:length_lines
    image = pixel_draw_line(image, 'white', list_lines{iter}, inner_radius);
end

end