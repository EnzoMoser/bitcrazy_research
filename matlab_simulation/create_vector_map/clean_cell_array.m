function result = clean_cell_array(cellArray)
    result = {};
    [~, jj] = size(cellArray);
    for i = 1:jj
        if iscell(cellArray{i})
            % If the current element is a cell, recurse into it
            result = [result, clean_cell_array(cellArray{i})]; %#ok<AGROW>
        elseif ~isempty(cellArray{i})
            % If the current element is not empty, add it to the result
            result = [result, cellArray{i}]; %#ok<AGROW>
        end
    end
end