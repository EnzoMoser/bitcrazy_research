function num = how_many_lines_has_point(point,list_of_lines)
num = 0;
if anynan(point) || ~iscell(list_of_lines)
    return
end
[~, list_length] = size(list_of_lines);
    for iter = 1:list_length
        line = list_of_lines{iter};
        if ismember(point, line, 'rows')
            num = num + 1;
        end
    end
    return
end