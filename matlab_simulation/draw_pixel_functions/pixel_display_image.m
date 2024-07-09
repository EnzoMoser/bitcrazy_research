function [] = pixel_display_image(image, figure_number)
figure(figure_number);
imshow(flipud(image),"Border","tight");
end