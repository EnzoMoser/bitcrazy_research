function torf = is_point_in_grid(point, grid_size)
% Must be positive
if anynan(point)
    torf = false;
    return
end
if point(1) >= 0 && point(1) <= grid_size && point(2) >= 0 && point(2) <= grid_size
    torf = true;
else
    torf = false;
end

end