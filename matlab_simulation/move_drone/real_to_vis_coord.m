function vis_drone_coord = real_to_vis_coord(drone_coord, offset_plus, offset_mult)
    vis_drone_coord = ceil( drone_coord * offset_mult ) + offset_plus;
end