function torf = is_point_in_lines(point,list_of_lines)
if anynan(point) || ~iscell(list_of_lines)
    torf = false;
    return
end
[~, list_length] = size(list_of_lines);
    for iter = 1:list_length
        line = list_of_lines{iter};
        if ismember(point, line, 'rows')
            torf = true;
            return
        end
    end
    torf = false;
    return
end