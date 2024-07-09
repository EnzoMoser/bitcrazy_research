function distance = get_distance(cur_coord, old_coord)
    distance = sqrt( ( cur_coord(1) - old_coord(1) )^2 + ( cur_coord(2) - old_coord(2) )^2 );
end