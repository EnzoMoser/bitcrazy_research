function list_of_coords = find_surrounding_coords(cur_coord,old_coord,grid_size,not_forward)
%Returns the coordinates of specific points surrounding a coordinate.
%Typically, the ones to its front and sides.

direction = get_direction(cur_coord, old_coord);

list_of_coords = [];

if abs(direction(1)) + abs(direction(2)) > 2
    error("Invalid Coordinates!!! The coordinates are not beside eachother!")
else
    angle = pi/4;
    rotation_matrix = [cos(angle) -sin(angle); sin(angle) cos(angle)];
    coord = round(direction * rotation_matrix) + cur_coord;
    if is_point_in_grid(coord, grid_size)
        list_of_coords = [list_of_coords; coord];
    end

    coord = direction + cur_coord;
    if (anynan(not_forward) || not_forward ~= true) && is_point_in_grid(coord, grid_size)
        list_of_coords = [list_of_coords; coord];
    end 

    angle = -pi/4;
    rotation_matrix = [cos(angle) -sin(angle); sin(angle) cos(angle)];
    coord = round(direction * rotation_matrix) + cur_coord;
    if is_point_in_grid(coord, grid_size)
        list_of_coords = [list_of_coords; coord];
    end

end

end