function [main_line, branch_lines, traffic_lights] = create_lines(grid_size, num_branches, main_line_op, branch_lines_op, limit_op)
% ____ OUTPUT VARS _____
%   - main_line => Size Nx2 Line that goes from start to finish.
%
%   - branch_lines => Cell array containing other lines of size Nx2 that...
%start randomly and merge unless given an end_point.
%
%   - traffic_lights => Cell array of Nx2 points that mark the...
%start and end of a line segment that does not touch any other lines.
%
% ____ INPUT VARS _____
%   - grid_size => Size of the grid the lines can move on. A size 20 would...
% mean the lines can move anywhere in a 21x21 area with coordinates 0 to 20.
% The lines will be doubled (this stops the traffic_lights var from being broken).
% This means it will output coordinates anywhere from 0 to 40 (instead of 20)
% Choose any positive integer.
%
%   - num_branches => The number of times the line will attempt to branch. The...
%function does not fail if the line fails to branch num_branches times. ...
% Tinker with other settings if the line is not branching enough.
% Choose any positive integer or zero.
%
%   - main_lines_op => A struct containing the parameters for the
%main_line. Leave an empty array for default values.
%
%   - branch_lines_op => A struct array for each containing the parameters...
% for each branch line. Leave an empty array for default values.
%
%   - limit_op => A struct containing the parameters for the limits when...
% generating a line.
% Leave an empty array for default values.

% ---- main_line_op ----
%   .start_point => the start point. must be within 0 and grid_size
%   .end_point => the end point.
%   .mid_point => the middle point. If not empty, it will go here first.
%   .random_length_from_start => the line will move randomly for this length, before...
% aiming for the mid_point or end_point
%   .random_length_from_mid => if there is a mid point and the line has passed it, it...
% will move randomly for this length before moving to end_point.

% ---- branch_lines_op(1) to branch_lines_op(N) ----
%   .mid_point
%   .end_point
%   .random_length_from_start
%   .random_length_from_mid
%   .wait => How long to wait from the last time the line has branched,
% before branching again.

% ---- limit_op ----
%   .full_restarts => If the line fails to generate, it will restart this
% number of times.
%   .limit => The max number of times a point can fail to generate.
%   .neg_limit => Everytime a point fails to generate, a the limit counter...
% goes down by neg_limit amount.
%   .limit_mult
%   .limit_exp
%
%   Every new point is given a new neg_limit. This is the equation:
%             neg_limit = ( (neg_limit^limit_exp) * limit_mult )


if isempty(grid_size)
    error("MUST SPECIFY GRID SIZE!!! (grid_size)")
end
if isempty(num_branches)
    error("MUST SPECIFY NUMBER OF BRANCHES!!! (num_branches)")
end

fake_grid_size = grid_size;

% ---- Default values for main_line_op and limit_op
start_point = [0 0];
mid_point = [NaN NaN];
end_point = [fake_grid_size fake_grid_size];
start_length = ceil(fake_grid_size*3/2);
mid_length = start_length;

full_restarts = 1;
limit = 50*fake_grid_size;
neg_limit = 2;
limit_mult = 1;
limit_exp = 1.1;
% ----

if isstruct(main_line_op)
    if isfield(main_line_op, 'start_point') && ~isempty(main_line_op.start_point) ; start_point = main_line_op.start_point; end
    if isfield(main_line_op, 'mid_point') && ~isempty(main_line_op.mid_point); mid_point = main_line_op.mid_point; end
    if isfield(main_line_op, 'end_point') && ~isempty(main_line_op.end_point); end_point = main_line_op.end_point; end
    if isfield(main_line_op, 'random_length_from_start') && ~isempty(main_line_op.random_length_from_start); start_length = main_line_op.random_length_from_start; end
    if isfield(main_line_op, 'random_length_from_mid') && ~isempty(main_line_op.random_length_from_mid); mid_length = main_line_op.random_length_from_mid; end
end

if isstruct(limit_op)
    if isfield(limit_op, 'full_restarts') && ~isempty(limit_op.full_restarts); full_restarts = limit_op.full_restarts; end
    if isfield(limit_op, 'max_limit') && ~isempty(limit_op.max_limit); limit = limit_op.max_limit; end
    if isfield(limit_op, 'counter_value') && ~isempty(limit_op.counter_value); neg_limit = limit_op.counter_value; end
    if isfield(limit_op, 'counter_multiple') && ~isempty(limit_op.counter_multiple); limit_mult = limit_op.counter_multiple; end
    if isfield(limit_op, 'counter_exponent') && ~isempty(limit_op.counter_exponent); limit_exp = limit_op.counter_exponent; end
end

bad_points = end_point;

if num_branches > 0
    distance = sqrt( ( end_point(1) - start_point(1) )^2 + ( end_point(2) - start_point(2) )^2 );
    wait_time = ceil(distance/(num_branches+3));

    for iter = 1:num_branches
        random_length = max(1, (start_length-(wait_time*iter) ) );

        % ---- Default values for all branch_lines_op(1:N)
        split_struct(iter).mid_point = [NaN NaN];
        split_struct(iter).real_end_point = [NaN NaN];
        split_struct(iter).start_length = random_length;
        split_struct(iter).mid_length = 0;
        split_struct(iter).wait = wait_time;
        % ----
        
        if ~isempty(branch_lines_op) && isstruct(branch_lines_op(iter)) && ~isempty(branch_lines_op(iter))
            if isfield(branch_lines_op, 'mid_point') && ~isempty(branch_lines_op(iter).mid_point)
                split_struct(iter).mid_point = branch_lines_op(iter).mid_point;
                bad_points = [bad_points; mid_point];
            end
            if isfield(branch_lines_op, 'end_point') && ~isempty(branch_lines_op(iter).end_point)
                split_struct(iter).real_end_point = branch_lines_op(iter).end_point;
                bad_points = [bad_points; end_point];
            end
            if isfield(branch_lines_op, 'random_length_from_start') && ~isempty(branch_lines_op(iter).random_length_from_start); split_struct(iter).start_length = branch_lines_op(iter).random_length_from_start; end %#ok<*AGROW>
            if isfield(branch_lines_op, 'random_length_from_mid') && ~isempty(branch_lines_op(iter).random_length_from_mid); split_struct(iter).mid_length = branch_lines_op(iter).random_length_from_mid; end 
            if isfield(branch_lines_op, 'wait') && ~isempty(branch_lines_op(iter).wait); split_struct(iter).wait = branch_lines_op(iter).wait; end 
        end
        
    end
else
    split_struct = [];
end

while full_restarts >= 0
    [main_line, ~, branch_lines] = create_point(start_point, [NaN NaN], {}, fake_grid_size, 0, NaN, start_length, mid_length, mid_point, end_point, limit, neg_limit, limit_mult, limit_exp, bad_points, split_struct, end_point);
    if ~anynan(main_line)
        disp("--- Line Successfully Made!!!---")
        break
    else
        if full_restarts <= 0
            disp("--- Line Generation Failed! Exiting....---")
        else
            disp("--- Line Generation Failed! Restarting....---")
        end
    end
    full_restarts = full_restarts - 1;
end

% Bring the main_line and branch_lines to the correct size.
if ~anynan(main_line)
    main_line = double_expand(main_line);
end

if ~isempty(branch_lines)
    [~, length_branch_lines] = size(branch_lines);
    for iter = 1:length_branch_lines
        branch_lines{iter} = double_expand(branch_lines{iter});
    end
end

traffic_lights = {};
if ~anynan(main_line) && ~isempty(branch_lines)
    % Find all branching points and all merging points.
    % Create traffic lights at the point after.

    all_traffic_points = [];
    all_lines = [ {main_line}, branch_lines];
    [~, length_all_lines] = size(all_lines);
    for iter = 1:length_all_lines
        ll = all_lines{iter};
        [length_ll, ~] = size(ll);
        for jk = 1:length_ll
            pp = ll(jk,:);
            if how_many_lines_has_point(pp, all_lines) > 1
                all_traffic_points((end+1),:) = pp;
            end
        end
        all_traffic_points((end+1),:) = ll(1,:);
        all_traffic_points((end+1),:) = ll(end,:);
    end

    all_traffic_points = unique(all_traffic_points,'rows');

    % Add traffic lights
    los_chips = {};
    for i = 1:length_all_lines
        one_line = all_lines{i};
        [length_one_line, ~ ] = size(one_line);
        one_line_traff_points = [];
        for j = 1:length_one_line
            one_point = one_line(j,:);
            if ismember(one_point, all_traffic_points, "rows")
                one_line_traff_points(end+1,:) = [j, one_point];
            end
        end

        [length_one_traff, ~ ] = size(one_line_traff_points);
        traff_n_not = [];
        for j = 1:length_one_traff
            index = one_line_traff_points(j,1);
            
            if index+1 <= length_one_line
                if ismember(one_line(index+1, :), one_line_traff_points(:, 2:3), "rows")
                    traff_n_not(end+1,:) = [ index+1, 0, one_line(index+1,:)];
                else
                    traff_n_not(end+1,:) = [ index+1, 1, one_line(index+1,:)];
                end
            end
            if ismember(one_line(), one_line_traff_points(:, 2:3))
                traff_n_not(end+1,:) = [ 0, one_line(index,:)];
            end
            if index-1 > 0
                if ismember(one_line(index-1, :), one_line_traff_points(:, 2:3), "rows")
                    traff_n_not(end+1,:) = [ index-1, 0, one_line(index-1,:)];
                else
                    traff_n_not(end+1,:) = [ index-1, 1, one_line(index-1,:)];
                end
            end
        end
        traff_n_not = sortrows(traff_n_not);

        traff_n_not = traff_n_not(:,2:end);

        a = 1;
        [z, ~] = size(traff_n_not);

        while a <= z
            if traff_n_not(a, 1) == 1
                if a+1 <= z
                    if traff_n_not(a+1, 1) == 1
                        pops = [ traff_n_not(a, 2:3); traff_n_not(a+1, 2:3) ];
                        a = a + 1;
                    else
                        pops = traff_n_not(a, 2:3);
                    end
                else
                    pops = traff_n_not(a, 2:3);
                end
                pops = unique(pops,'rows');
                los_chips{end+1} = pops;
            end
            a = a + 1;
        end
    end
    traffic_lights = los_chips;
end
    
end