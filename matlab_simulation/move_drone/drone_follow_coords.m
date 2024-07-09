function [ torf, vis_drone_coord, drone_coord ] = drone_follow_coords(vis_img, img, path, drone_coord, drone_radius, move_length, drone_color, bad_drone_color, time_delay, offset_plus, offset_mult, allowed_colors, pseudo_fig, vis_fig)

torf = true;
[ pa_len, ~ ] = size(path);

d = path(2:end, :) - path(1:end-1, :);

dis_all(drone_color, drone_coord, path(1,:))

for iter = 2:pa_len

test_drone_coord = ( d(iter-1,:) * move_length) + drone_coord;
test_vis_drone_coord = real_to_vis_coord(test_drone_coord, offset_plus, offset_mult);

if pixel_valid_area(img, test_drone_coord, drone_radius, allowed_colors)
    dis_all(drone_color, test_drone_coord, test_vis_drone_coord)
    drone_coord = test_drone_coord;
    vis_drone_coord = test_vis_drone_coord;
    torf = true;
else
    dis_all(drone_color, test_drone_coord, test_vis_drone_coord)
    dis_all(bad_drone_color, test_drone_coord, test_vis_drone_coord)
    error("THIS ERROR SHOULDN'T HAVE HAPPENED!!!")
    torf = false;
end
pause(time_delay)

end

    function dis_all(cor, coord, vis_coord)
        new_img = pixel_draw_circle(img, coord, drone_radius, cor);
        new_vis_img = set_pixel_color(vis_img, vis_coord, cor);
        if time_delay > 0
            pixel_display_image(new_img, pseudo_fig);
            pixel_display_image(new_vis_img, vis_fig);
        end
        pause(time_delay)
    end

end