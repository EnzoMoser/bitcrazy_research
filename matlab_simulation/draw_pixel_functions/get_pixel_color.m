function color = get_pixel_color(vis_img, coord)
 color = zeros(1,3);
 color(1,:) = vis_img(coord(2), coord(1), :);
end