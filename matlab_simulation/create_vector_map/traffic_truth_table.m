function truth_table = traffic_truth_table(segments, start_point, end_point)
% Return all configurations that allow for a line to go from start_point to
% end_point

% Check how many segs have start_point.

% Check how many segs have the end this seg

% To create a truth table, follow the maze solving pattern.
% Recursive function. When given more than one line, create two new functions.
% One for each line.
% Make sure to not go over the same line in a given recursive attempt.

% The function returns empty if it reaches a dead end or goes over a line
% it already went over.
% The function returns the index in segments{index} if it finds the
% end_point.

truth_table = {};

[~, idxs] = which_lines_have_point(start_point, segments);

[lef, ~] = size(idxs);
for iter = 1:lef
    index = idxs(iter);
    if isequal(start_point, segments{index}(1,:))
        new_reverse = false;
    else
        new_reverse = true;
    end
    trya = recursive_truth(segments, index, [], end_point, new_reverse); 
    truth_table{end+1} = trya; %#ok<AGROW>
end

% Start the traversal with the top-level truth_table
truth_table = clean_cell_array(truth_table);

end