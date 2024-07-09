function path = bfs_path(image, start_coord, end_coord, allowed_colors)
    startRow = start_coord(1);
    startCol = start_coord(2);

    endRow = end_coord(1);
    endCol = end_coord(2);

    % Directions for moving in 4-connected grid (up, down, left, right)
    directions = [0 1; 1 0; 0 -1; -1 0];
    
    % Initialize the queue for BFS
    queue = [startRow, startCol];
    
    % Initialize the visited matrix
    visited = false(size(image));
    visited(startRow, startCol) = true;
    
    % Initialize the parent matrix to reconstruct the path
    parent = cell(size(image));
    parent{startRow, startCol} = [startRow, startCol];
    
    % Perform BFS
    while ~isempty(queue)
        current = queue(1, :);
        queue(1, :) = []; % Dequeue
        
        % Check if we have reached the end pixel
        if current(1) == endRow && current(2) == endCol
            break;
        end
        
        % Explore the neighbors
        for i = 1:size(directions, 1)
            newRow = current(1) + directions(i, 1);
            newCol = current(2) + directions(i, 2);
            
            % Check if the new position is within bounds and is a white pixel
            if newRow >= 1 && newRow <= size(image, 1) && ...
               newCol >= 1 && newCol <= size(image, 2) && ...
               ~visited(newRow, newCol)
               check_color = get_pixel_color(image, [newRow, newCol] );
               if ismember(check_color, allowed_colors, 'rows')
                % Mark as visited and enqueue
                visited(newRow, newCol) = true;
                queue = [queue; newRow, newCol];
                parent{newRow, newCol} = current;
               end
            end
        end
    end
    
    % Reconstruct the path
    if ~visited(endRow, endCol)
        path = [];
        disp('No path found.');
    else
        path = [endRow, endCol];
        while ~isequal(parent{path(1,1), path(1,2)}, [startRow, startCol])
            path = [parent{path(1,1), path(1,2)}; path];
        end
        path = [[startRow, startCol]; path];
    end
end
