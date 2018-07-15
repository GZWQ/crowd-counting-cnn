
load('vidf1_33_roi_mainwalkway.mat');
im = imread('IMG_1.jpg');
[h, w, c] = size(im); %h=160,w=240
if (c == 3)
im = rgb2gray(im);
end
[h, w, c] = size(im);
im_den1 = zeros(size(im));
im_den2 = zeros(size(im));
x = roi.xi;
y = roi.yi;
area = roi.mask;
[xx,yy] = size(area);
imwrite(area,'mask.jpg');

% for i = 1:h
%     tf1 = ismember(i,floor(x));
%     if (tf1==1)
%         for j = 1:w
%             im_den1(i,j)=1;
%           
%   
%         end
%     end
% end
% imwrite(im_den1,'out1.jpg');
% for j = 1:w
%     tf1 = ismember(i,floor(y));
%     if (tf1==1)
%         for i = 1:h
%             im_den2(i,j)=1;
%           
%   
%         end
%     end
% end
% 
% imwrite(im_den2,'out2.jpg');
