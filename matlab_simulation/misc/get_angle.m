function angle = get_angle(cur_coord, old_coord)
direc = get_direction(cur_coord, old_coord);
angle = atan2(direc(2), direc(1));
end