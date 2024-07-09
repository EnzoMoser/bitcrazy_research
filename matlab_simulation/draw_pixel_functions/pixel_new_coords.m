function coords = pixel_new_coords(coords, image_size, max_line_coord, border)

coords = round( coords * ( (image_size-2*border) / max_line_coord ) ) + border;

end