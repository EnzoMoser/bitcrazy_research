function [] = vector_display_lines(seg_lines,grid_size,figure_number)
%VECTOR_DISPLAY_LINES Summary of this function goes here
%   Detailed explanation goes here

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

figure(figure_number);
hold on;
axis([-1 grid_size+1 -1 grid_size+1]);
xticks(0:grid_size);
yticks(0:grid_size);
grid on;
xlabel('X');
ylabel('Y');

[~, length_all_lines] = size(seg_lines);

for iter = 1:length_all_lines
    % Plot the points and connect them with lines
    single_line = seg_lines{iter};
    for i = 1:size(single_line, 1)-1
        % Plot the line connecting current point to the next point
        plot([single_line(i, 1), single_line(i+1, 1)], [single_line(i, 2), single_line(i+1, 2)], 'b-', 'LineWidth', 2);
    end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Plot all the points
colorstring = 'rgbcmykw';
sed = 1;
for o = 1:length_all_lines
    ll = seg_lines{o};
    plot(ll(2,1), ll(2,2), 'ro', 'MarkerSize', 10, 'MarkerFaceColor', colorstring(sed));
    plot(ll(end-1,1), ll(end-1,2), 'ro', 'MarkerSize', 10, 'MarkerFaceColor', colorstring(sed));
    sed = sed+1;
    if sed > 8; sed = 1; end
end

hold off;

end