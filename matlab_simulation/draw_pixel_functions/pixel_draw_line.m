function image = pixel_draw_line(image, color, coords, radius)
%PIXEL_CURVED_LINE Output a line with a rounded end.
[len_c, ~ ] = size(coords);

if len_c ~= 1
    for iter = 2:len_c
        direc = get_direction(coords(iter,:), coords(iter-1,:));
        angle = atan2(direc(2), direc(1));
        perpangle = angle+(pi/2);
    
        mult = round ( [ cos(perpangle), sin(perpangle) ] .* radius );
    
        points = [ coords(iter-1,:)+mult, coords(iter-1,:)-mult, coords(iter,:)-mult, coords(iter,:)+mult ];
    
        image = insertShape(image, 'filled-polygon', points, 'Color', color, 'SmoothEdges', false, 'Opacity', 1);
        image = insertShape(image, 'filled-circle', [coords(iter-1,1), coords(iter-1,2), radius], 'ShapeColor', color, 'SmoothEdges', false, 'Opacity', 1);
        image = insertShape(image, 'filled-circle', [coords(iter,1), coords(iter,2), radius], 'ShapeColor', color, 'SmoothEdges', false, 'Opacity', 1);
    end
else
    image = insertShape(image, 'filled-circle', [coords(1), coords(2), radius], 'ShapeColor', color, 'SmoothEdges', false, 'Opacity', 1);
end

end