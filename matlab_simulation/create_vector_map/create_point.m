function [future_n_cur_points, bad_points, branch_lines ] = create_point(cur_coord, prev_points, other_lines, grid_size, line_length, mid_line_length, start_length, mid_length, mid_point, real_end_point, limit, neg_limit, limit_mult, limit_exp, bad_points, split_struct, original_end_point)
% If length is defined, it will go for length and fail on end point. Otherwise, it will look for
% end point.

branch_lines = {};
if ~isempty(split_struct)
    split_struct(1).wait = split_struct(1).wait - 1;
end

check_merge = false;
is_length_limited = true;

if ~anynan(mid_point)
    end_point = mid_point;
else
    if ~anynan(real_end_point)
        end_point = real_end_point;
    else
        end_point = original_end_point;
        check_merge = true;
    end
end

if line_length >= start_length
    if ~anynan(mid_line_length)
        if ~anynan(real_end_point)
            end_point = real_end_point;
        else
            end_point = original_end_point;
        end
        if (line_length - mid_line_length) > mid_length
            is_length_limited = false;
        end
    else
        is_length_limited = false;
    end
end

if check_merge && ~is_length_limited
    merge_allowed = true;
else
    merge_allowed = false;
end

if isequal(cur_coord, end_point)
    if (~anynan(bad_points))
        [row_index, ~] = ismember(cur_coord, bad_points, "rows");
        if ~isempty(row_index)
            bad_points(row_index, :) = [];
        end
    end
    if ~anynan(mid_point) && isequal(end_point, mid_point)
        mid_point = [NaN NaN];
        mid_line_length = line_length;
        if ~anynan(real_end_point)
            end_point = real_end_point;
        else
            end_point = original_end_point;
        end
    else
        future_n_cur_points = cur_coord;
        return
    end
   
end

if (~anynan(bad_points))
    [length_bad, ~] = size(bad_points);
    for iter = 1:length_bad
        if isequal(cur_coord, bad_points(iter,:))
            isequal(cur_coord, end_point)
            future_n_cur_points = [NaN NaN];
            return
        end
    end
end
 
if merge_allowed && is_point_in_lines(cur_coord, other_lines)
    %disp("---MERGED!")
    future_n_cur_points = cur_coord;
    return
end

if ~anynan(prev_points)
    [ ~, points_length ] = size(prev_points);
else
    points_length = 0;
end

if points_length <= 0
    possible_moves = [ [0 1]; [0 -1]; [1 0]; [-1 0]; [1 1]; [1 -1]; [-1 1]; [-1 -1] ];
    possible_moves = possible_moves + cur_coord;

else
    old_coord = prev_points(end, :);
    possible_moves = find_surrounding_coords(cur_coord, old_coord, grid_size, NaN);
end

if isempty(possible_moves) || limit <= 0
    future_n_cur_points =[NaN NaN];
    %disp("No More Moves!")
    return
end

% If undefined line length, randomize order. Otherwise, bias towards the
% end point.
[ length_moves, ~ ] = size(possible_moves);
if is_length_limited
    possible_moves = possible_moves(randperm(length_moves), :);
else
    distances = zeros(1,length_moves);
    for iter = 1:1:length_moves
        d = sqrt( ( end_point(1) - possible_moves(iter, 1) )^2 + ( end_point(2) - possible_moves(iter, 2) )^2 );
        distances(iter) = d;
    end
    [~, mov_id] = sort(distances);
    possible_moves = possible_moves(mov_id, :);
end

% Setup for the loop below:
iter = 1;
[ moves_num, ~ ] = size(possible_moves);

line_length = line_length+1;

if ~anynan(prev_points)
    prev_n_cur_points = [prev_points; cur_coord];
else
    prev_n_cur_points = cur_coord;
end

% Start with the first move on the list. If the move fails, go to the next
% one. Exit with NaN if it fails all of them, or if the limit reaches zero.
%
% If a move succeeds, exit successfully.
if iter > moves_num && limit < 0
    %disp("NO SHOT!")
    future_n_cur_points = [NaN NaN];
    return
end
while true
    new_coord = possible_moves(iter, :);

    if ( anynan(prev_points) || ~ismember(new_coord,prev_points,'rows') )...
            && ( merge_allowed || ~is_point_in_lines(new_coord, other_lines) )...
            && ~(is_diagonal(new_coord, cur_coord) && do_lines_cross(new_coord, cur_coord, prev_points, other_lines, grid_size))

        if iter >= moves_num || isempty(split_struct) || split_struct(1).wait >= 0
            [future_points, future_bad_points, future_branch_lines] = create_point(new_coord, prev_n_cur_points, other_lines, grid_size, line_length, mid_line_length, start_length, mid_length, mid_point, real_end_point, ceil(limit), ((neg_limit^limit_exp)*limit_mult), limit_mult, limit_exp, bad_points, split_struct, original_end_point);
            if ~anynan(future_points)
                future_n_cur_points = [cur_coord; future_points];
                bad_points = future_bad_points;
                branch_lines = future_branch_lines;
                return
            end
        else
            % Split the split_struct and create two lines with an equal
            % amount. One will have a true value for reaching the end.
            % If must_reach_end is false, it can merge with other lines
            % If at a certain length
            [~, length_struct] = size(split_struct);
            length_struct = length_struct - 1;
            if length_struct == 0
                split_struct_one = [];
                split_struct_two = [];
            elseif length_struct == 1
                split_struct_one = split_struct(2:end, :);
                split_struct_two = [];
            else
                half = (ceil(length_struct/2) + 1);
                split_struct_one = split_struct(2:half);
                split_struct_two = split_struct((half+1):end);
            end

            [ break_line_one, break_bad_points_one, other_branches_one ] = create_point(new_coord, prev_n_cur_points, other_lines, grid_size, line_length, mid_line_length, start_length, mid_length, mid_point, real_end_point, ceil(limit), ((neg_limit^limit_exp)*limit_mult), limit_mult, limit_exp, bad_points, split_struct_one, original_end_point );
            if ~anynan(break_line_one)
                iter = iter + 1;
                new_coord = possible_moves(iter, :);
                if ~anynan(prev_points)
                    future_other_lines = [ {prev_points}, other_lines, other_branches_one, {break_line_one} ];
                else
                    future_other_lines = [ other_lines, other_branches_one, {break_line_one} ];
                end

                if ( anynan(prev_points) || ~ismember(new_coord,prev_points,'rows') )...
            && ( merge_allowed || ~is_point_in_lines(new_coord, future_other_lines) )...
            && ~(is_diagonal(new_coord, cur_coord) && do_lines_cross(new_coord, cur_coord, prev_points, future_other_lines, grid_size))

                    future_bad_points = break_bad_points_one;
                    [ break_line_two, break_bad_points_two, other_branches_two ] = create_point(new_coord, cur_coord, future_other_lines, grid_size, 0, NaN, split_struct(1).start_length, split_struct(1).mid_length, split_struct(1).mid_point, split_struct(1).real_end_point, ceil(limit), ((neg_limit^limit_exp)*limit_mult), limit_mult, limit_exp, future_bad_points, split_struct_two, original_end_point );
                    if ~anynan(break_line_two)
                        % All branches successfully generated
                        future_n_cur_points = [cur_coord; break_line_one];
                        bad_points = break_bad_points_two;
                        branch_lines = [{[ cur_coord; break_line_two ]}, other_branches_one, other_branches_two];
                        return
                    end
                end
            end
        end
    end

    iter = iter+1;
    limit = limit-neg_limit;

    if iter > moves_num
        %disp("MOVES REACHED!")
        future_n_cur_points = [NaN NaN];
        return
    elseif limit < 0
        %disp("LIM REACHED!")
        future_n_cur_points = [NaN NaN];
        return    
    end
end

end