%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% File to create grount truth density map for test set%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc;
image_path = ['../data/original/ucsd/test_data/images/'];
gt_path = ['../data/original/ucsd/test_data/ground_truth/'];
out_gt_path_csv = ['../data/original/ucsd/test_data/gt_truth_csv/'];

mkdir(out_gt_path_csv);
num_images_1 = 2; % [0,1,2] + [3,4,5,6] 
num_images_2 = 9; % [7,8,9]
load([gt_path,'vidf1_33_roi_mainwalkway.mat']);

for i = 0:num_images_1
    fprintf(1,'Processing %3d/%d files\n', i, num_images_1);
    gt_file_name = [gt_path,'vidf1_33_00',num2str(i),'_frame_full.mat'];
    load(gt_file_name);
    for t = 1:200
        pic_num = i*200+t;
        disp(pic_num);
        input_img_name = strcat(image_path,'IMG_',num2str(pic_num),'.jpg');
        im = imread(input_img_name);
        [h, w, c] = size(im);
        
        if (c == 3)
        im = rgb2gray(im);
        end  
        annPoints =  frame{t}.loc;
        im_density = ucsd_density_map(im,annPoints,roi.xi,roi.yi);
        csvwrite([out_gt_path_csv ,'IMG_',num2str(pic_num),'.csv'], im_density);
    end      
     
end

for i = 7:num_images_2
    fprintf(1,'Processing %3d/%d files\n', i, num_images_2);
    gt_file_name = [gt_path,'vidf1_33_00',num2str(i),'_frame_full.mat'];
    load(gt_file_name);
    for t = 1:200
        pic_num = (i-4)*200+t;
        disp(pic_num);
        input_img_name = strcat(image_path,'IMG_',num2str(pic_num),'.jpg');
        im = imread(input_img_name);
        [h, w, c] = size(im);
        
        if (c == 3)
        im = rgb2gray(im);
        end  
        annPoints =  frame{t}.loc;
        im_density = ucsd_density_map(im,annPoints,roi.xi,roi.yi);    
        csvwrite([out_gt_path_csv ,'IMG_',num2str(pic_num),'.csv'], im_density);
    end      
     
end
