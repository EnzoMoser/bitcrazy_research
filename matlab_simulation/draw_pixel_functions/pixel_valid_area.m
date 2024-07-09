function torf = pixel_valid_area(image, center, radius, allow_color_list)

good_color_count = 0;
bad_color_count = 0;

[image_length, ~, ~] = size(image);

da_xxx = center(1);
da_yyy = center(2);

% Create area
if da_xxx-radius < 1
    bot_xxx = 1;
else
    bot_xxx = da_xxx - radius;
end

if da_yyy-radius < 1
    bot_yyy = 1;
else
    bot_yyy = da_yyy - radius;
end

if da_xxx+radius > image_length
    up_xxx = image_length;
else
    up_xxx = da_xxx + radius;
end

if da_yyy+radius > image_length
    up_yyy = image_length;
else
    up_yyy = da_yyy + radius;
end

for check_xxx = bot_xxx:up_xxx
for check_yyy = bot_yyy:up_yyy
    dist = sqrt((check_xxx - center(1))^2 + (check_yyy - center(2))^2);
    % Check for circle radius.
    if dist <= radius
        % Check for color in circle.
        pixel = squeeze(image(check_yyy, check_xxx, :))';
        if ismember(pixel, allow_color_list, 'rows')
            good_color_count = good_color_count + 1;
        else
            bad_color_count = bad_color_count + 1;
        end
    end
end
end

if good_color_count >= bad_color_count
    torf = true;
else
    torf = false;
end

end