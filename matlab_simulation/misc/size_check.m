function [big_a, small_a] = size_check(drone_coord, big_a, small_a)

if drone_coord(1) < small_a
    small_a = drone_coord(1);
elseif drone_coord(1) > big_a
    big_a = drone_coord(1);
end

if drone_coord(2) < small_a
    small_a = drone_coord(2);
elseif drone_coord(2) > big_a
    big_a = drone_coord(2);
end

end