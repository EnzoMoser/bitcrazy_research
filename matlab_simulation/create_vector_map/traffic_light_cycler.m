function image = traffic_light_cycler(image, segments, truth_table, truth_table_index, radius, green_color, red_color)
    truth_line = truth_table{truth_table_index};

    [~, hh] = size(segments);
    for iter = 1:hh
        seg = segments{iter};
        traff_one = seg(2,:);
        traff_two = seg(end-1,:);
        if ismember(iter, truth_line)
            % Print green or white
            image = pixel_draw_circle(image, traff_one, radius, green_color);
            image = pixel_draw_circle(image, traff_two, radius, green_color);
        else
            % Print red
            image = pixel_draw_circle(image, traff_one, radius, red_color);
            image = pixel_draw_circle(image, traff_two, radius, red_color);
        end
    end
end