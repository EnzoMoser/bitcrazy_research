function torf = do_lines_cross(cur_coord, old_coord, line, other_lines, grid_size)
% To prevent diagonal crosses, this function checks itself and all other lines to see if has accidentally
% crossed over any of them.

direction = get_direction(cur_coord, old_coord);
cur_coord = old_coord - direction;
diag_points = find_surrounding_coords(old_coord, cur_coord, grid_size, true);

if iscell(other_lines)
    if ~anynan(line)
        other_lines{end+1} = line;
    end
else
    other_lines = {line};
end

[~, list_length] = size(other_lines);
for iter = 1:list_length

    loon = other_lines{iter};

    [~, index] = ismember(diag_points(1,:), loon, "rows");
    
    if isempty(index)
        continue
    end

    [line_length, ~] = size(loon);
    
    if index < line_length && isequal(diag_points(2,:),loon(index+1,:))
        torf = true;
        return
    end
    
    if index > 1 && isequal(diag_points(2,:),loon(index-1,:))
        torf = true;
        return
    end

end


torf = false;
end