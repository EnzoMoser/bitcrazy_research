function [ic_present, idc] = which_lines_have_point(point,list_lines)
ic_present = false;
idc = [];

[~, len_list] = size(list_lines);

for iter = 1:len_list
[is_present, ~] = ismember(point, list_lines{iter}, 'rows');
    if is_present
        idc(end+1,:) = iter; %#ok<AGROW>
        ic_present = true;
    end
end

end