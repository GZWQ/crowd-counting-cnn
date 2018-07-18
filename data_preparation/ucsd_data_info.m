clc;
load('vidf1_33_roi_mainwalkway.mat');

im = imread('IMG_1.jpg');

[h, w, c] = size(im);
        
if (c == 3)
im = rgb2gray(im);
end  

mask_area = uint8(roipoly(im,floor(roi.xi),floor(roi.yi)));

im_a = im.*uint8(mask_area);
imshow(im_a);