H = fspecial('Gaussian',[15, 15],0.3);
load('vidf1_33_roi_mainwalkway.mat');
mask = roi.mask;
im = imread('IMG_2.jpg');

x = roi.xi;
y = roi.yi;
[h, w, c] = size(im);
if (c == 3)
im = rgb2gray(im);
end
bw = roipoly(im,floor(x),floor(y));
im1 = zeros(size(bw));
im1(1,2) = 1;
JJ = roifilt2(H,im1(1:158,1:238),mask);
disp(sum(sum(H)));
disp(sum(sum(im(1:158,1:238))));
disp(sum(sum(JJ)));




