function [ vis_img, vis_drone_coord, offset_plus, offset_mult, drone_coord ] = scan_area(img, drone_coord, drone_radius, time_delay,...
    move_length, allowed_colors, drone_color, bad_drone_color, ...
    line_color, border_color, vis_border, vis_starting_size, vis_increase_size, ...
    unknown_color, ...
    cur_loc_color, real_fig, vis_fig)

vis_start_coord = 1 + ceil(vis_starting_size / 2);
vis_drone_coord = [vis_start_coord vis_start_coord];

vis_size = vis_starting_size+(2*vis_border);
add_to_offset = 0;

vis_img = zeros(vis_size, vis_size, 'uint8');
vis_img(:, :, 1) = unknown_color(1);
vis_img(:, :, 2) = unknown_color(2);
vis_img(:, :, 3) = unknown_color(3);

a_small = vis_border + 1;
a_big = vis_starting_size - 1 - vis_border;
real_big_v = max( drone_coord(1), drone_coord(2) );
real_small_v = min( drone_coord(1), drone_coord(2) );
sa_old = a_small;
ba_old = a_big;

or_to_vis_mult = ( 1 / move_length );
or_to_vis_offset = vis_drone_coord - ceil( or_to_vis_mult * drone_coord );

if time_delay > 0; pixel_display_image(vis_img, vis_fig); end

check_all = [ 1 0 0; -1 0 pi; 0 1 pi/2; 0 -1 pi*3/2];

stack = [vis_drone_coord, 0];

while ~isempty(stack)
    da_list = check_all + [ stack(end,1:2), 0 ] ;
    next_coord = [];
    for iter = 1:4
        [ stack(:, 1:2), da_list(iter, 1:2) ] = check_vis_img_sizes( stack(:, 1:2), da_list(iter, 1:2) );
        cor = get_pixel_color(vis_img, da_list(iter, 1:2) );
        if isequal(cor, unknown_color)
            next_coord = da_list(iter, :);
            break
        end
    end
    if ~isempty(next_coord)
        [ successfull_step, test_drone_coord ] = drone_try_move_n_display(true, img, drone_coord, drone_radius, time_delay, ...
                    move_length, next_coord(1,3), allowed_colors, drone_color, bad_drone_color, real_fig);

        vis_test_drone_coord = ceil( test_drone_coord * or_to_vis_mult ) + or_to_vis_offset;

        [ real_big_v, real_small_v ] = size_check(test_drone_coord, real_big_v, real_small_v);

        if successfull_step
            vis_drone_coord = vis_test_drone_coord;
            drone_coord = test_drone_coord;
            stack(end+1,:) = next_coord; %#ok<AGROW>
            use_color = line_color;
        else
            use_color = border_color;
        end

        vis_img = set_pixel_color(vis_img, vis_test_drone_coord, use_color);
        if time_delay > 0;  pixel_display_image(set_pixel_color(vis_img, vis_drone_coord, cur_loc_color), vis_fig); end

    else
        hangle = stack(end,3) + pi;
        stack(end,:) = [];

        [ successfull_step, test_drone_coord ] = drone_try_move_n_display(true, img, drone_coord, drone_radius, time_delay, ...
                    move_length, hangle, allowed_colors, drone_color, bad_drone_color, real_fig);
        vis_drone_coord = ceil( test_drone_coord * or_to_vis_mult ) + or_to_vis_offset;
        drone_coord = test_drone_coord;
        if ~successfull_step
            error("EERROROROOROR");
        end
    end
end

%%
% Shrink the map

vis_a_big = ceil( real_big_v * or_to_vis_mult ) + or_to_vis_offset(1);
vis_a_small = floor( real_small_v * or_to_vis_mult ) + or_to_vis_offset(1);

st = max(vis_border, (vis_a_small-vis_border));
et = min(vis_size-vis_border, (vis_a_big+vis_border));

new_vis_img = vis_img( st:et, st:et, :);
vis_img = new_vis_img;

or_to_vis_offset = or_to_vis_offset - st + 1;
vis_drone_coord = vis_drone_coord - st + 1;
[ vis_size, ~, ~ ] = size(vis_img);
a_small = vis_border + 1;
a_big = vis_size - vis_border;

%%
% Ending notes.

offset_plus = or_to_vis_offset;
offset_mult = or_to_vis_mult;

%%
% Other functions

% Function to update the image size and coordinates if the visual image is
% too small.
function [ vis_list, specific_coord ] = check_vis_img_sizes(vis_list, specific_coord)
        if isempty(specific_coord)
            [ len_list, ~ ] = size(vis_list);
            for jjj = 1:len_list
                check_me = vis_list(jjj, :);
                if check_me(1) < a_small
                    a_small = check_me(1);
                elseif check_me(1) > a_big
                    a_big = check_me(1);
                end
                if check_me(2) < a_small
                    a_small = check_me(2);
                elseif check_me(2) > a_big
                    a_big = check_me(2);
                end
            end
        else
            if specific_coord(1) < a_small
                a_small = specific_coord(1);
            elseif specific_coord(1) > a_big
                a_big = specific_coord(1);
            end
            if specific_coord(2) < a_small
                a_small = specific_coord(2);
            elseif specific_coord(2) > a_big
                a_big = specific_coord(2);
            end
        end

        if a_big > ba_old || a_small < sa_old
        new_vis_size = ( vis_size * vis_increase_size);
        new_vis_img = zeros(new_vis_size, new_vis_size, 'uint8');
        new_vis_img(:, :, 1) = 80;
        new_vis_img(:, :, 2) = 80;
        new_vis_img(:, :, 3) = 180;

        add_to_offset = ceil( (new_vis_size - vis_size)/4 );

        st = add_to_offset+1;
        et = add_to_offset+vis_size;

        new_vis_img( st:et, st:et, :) = vis_img;

        vis_img = new_vis_img;
        vis_drone_coord = vis_drone_coord + add_to_offset;
        vis_list = vis_list + add_to_offset;
        or_to_vis_offset = or_to_vis_offset + add_to_offset;
        vis_size = new_vis_size;
        a_small = vis_border + 1;
        a_big = new_vis_size - vis_border;
        if ~isempty(specific_coord)
            specific_coord = specific_coord + add_to_offset;
        end
        ba_old = a_big;
        sa_old = a_small;
        end
    end

end