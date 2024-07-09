function torf = is_diagonal(cur_coord,old_coord)
if abs( cur_coord(1) - old_coord(1) ) + abs( cur_coord(2) - old_coord(2) ) == 2
    torf = true;
else
    torf = false;
end

end