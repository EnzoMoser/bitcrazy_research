function [ torf, new_drone_coord ] = drone_try_move_n_display(go_back_if_unsuccessful, image, drone_coord, drone_radius, time_delay, move_length, move_angle, allowed_colors, drone_color, bad_drone_color, real_fig)

new_drone_coord = drone_move(drone_coord, move_length, move_angle);

if pixel_valid_area(image, new_drone_coord, drone_radius, allowed_colors)
    new_image = pixel_draw_circle(image, new_drone_coord, drone_radius, drone_color);
    if time_delay > 0; pixel_display_image(new_image, real_fig); end
    torf = true;
elseif go_back_if_unsuccessful
    new_image = pixel_draw_circle(image, new_drone_coord, drone_radius, bad_drone_color);
    if time_delay > 0; pixel_display_image(new_image, real_fig); end
    pause(time_delay)
    new_image = pixel_draw_circle(image, drone_coord, drone_radius, drone_color);
    if time_delay > 0; pixel_display_image(new_image, real_fig); end
    torf = false;
else
    new_image = pixel_draw_circle(image, new_drone_coord, drone_radius, bad_drone_color);
    if time_delay > 0; pixel_display_image(new_image, real_fig); end
    torf = false;
end
pause(time_delay)

end