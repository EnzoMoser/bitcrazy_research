function truth_table = recursive_truth(segments, starting_segment, already_visited, end_point, reverse)

% segments{index}
% already_visited[Nx1] are the indexes
% end_point[1x2]

truth_table = {};

if ismember(end_point, segments{starting_segment}, 'rows')
    already_visited(end+1,:) = starting_segment;
    truth_table = already_visited;
    return
end

if ismember(starting_segment, already_visited)
    return
end

already_visited(end+1,:) = starting_segment;

if reverse
    edge = segments{starting_segment}(1,:);
else
    edge = segments{starting_segment}(end,:);
end

[~, idxs] = which_lines_have_point(edge, segments);

[lef, ~] = size(idxs);

for iter = 1:lef
    index = idxs(iter,1);
    if ~ismember(index, already_visited)
        if isequal(edge, segments{index}(1,:))
            new_reverse = false;
        else
            new_reverse = true;
        end
        trya = recursive_truth(segments, index, already_visited, end_point, new_reverse);
        if ~isempty(trya)
            truth_table{end+1} = trya; %#ok<AGROW>
        end
    end
end

[~, gg] = size(truth_table);
if gg == 1
    truth_table = truth_table(1);
end

end