function [doubled_line] = double_expand(line)
[length_line, ~] = size(line);
doubled_line = zeros( ((length_line*2)-1), 2);

iter = 1;

while iter < length_line
    doubled_line(2*iter-1,:)=2*line(iter,:);
    doubled_line(2*iter,:)=get_direction( line(iter+1,:), line(iter,:) ) + 2*line(iter,:);

    iter = iter + 1;
end

doubled_line(end,:) = 2*line(end,:);

end