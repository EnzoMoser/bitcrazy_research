function new_img = pixel_draw_circle(image, coordinate, radius, color)
% Draw a circle
new_img = insertShape(image, 'filled-circle', [coordinate(1), coordinate(2), radius], 'ShapeColor', color, 'SmoothEdges', false, 'Opacity', 1);
end