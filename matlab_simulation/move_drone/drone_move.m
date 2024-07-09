function new_drone_coord = drone_move(drone_coord, move_length, move_angle)

    mult = round ( [ cos(move_angle), sin(move_angle) ] .* move_length );
    new_drone_coord = drone_coord + mult;

end