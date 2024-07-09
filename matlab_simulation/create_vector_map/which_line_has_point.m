function [line, idx] = which_line_has_point(point,list_lines)
line = [];

[~, len_list] = size(list_lines);

for iter = 1:len_list
    % disp("APP")
    % disp(point)
    % disp("NUTS")
    % disp(list_lines{iter})
[is_present, idx] = ismember(point, list_lines{iter}, 'rows');
    if is_present
        line = list_lines{iter};
        break
    end
end

end