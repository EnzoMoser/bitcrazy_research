function vis_img = set_pixel_color(vis_img, coord, color)
    vis_img(coord(2), coord(1), :) = color;
end