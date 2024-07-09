function line_segments = segment_lines(main_line, branch_lines, traffic_lights)
%SEGMENT_LINE Converts the lines into line segments based on the...
% location of traffic points

% segment = line_segments{iter}
% segment(2,:) and segment(end-1,:) are the traffic lights for the line.

if isempty(branch_lines)
    line_segments = { main_line };
    return
end

all_lines = [{main_line}, branch_lines];

[~, length_traffic] = size(traffic_lights);

line_segments = cell(1, length_traffic);

for iter = 1:length_traffic
    light = traffic_lights{iter};
    [light_len, ~] = size(light);
    [line, id_one] = which_line_has_point(light(1,:), all_lines);
    if light_len == 2
        % 2 points
        [is_present, id_two] = ismember(light(2,:), line, 'rows');
        if is_present
            order = [id_one; id_two];
            order = sortrows(order);
            man = line(order(1,:)-1:order(2,:)+1,:);
        else
            man = line(id_one-1:id_one+1,:);
        end
    else
        % 1 point
        man = line(id_one-1:id_one+1,:);
    end

    line_segments{iter} = man;
end

end