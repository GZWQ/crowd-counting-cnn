%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% File to create grount truth density map for test set%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


clc; 
dataset = 'A';
dataset_name = ['shanghaitech_part_' dataset ];
path = ['../data/original/shanghaitech/part_' dataset '_final/test_data/images/'];
gt_path = ['../data/original/shanghaitech/part_' dataset '_final/test_data/ground-truth/'];
gt_path_csv = ['../data/original/shanghaitech/part_' dataset '_final/test_data/ground_truth_csv/'];

mkdir(gt_path_csv);
if (dataset == 'A')
    num_images = 182;
else
    num_images = 316;
end

gt_people_count = [];

for i = 1:num_images  
    if (mod(i,10)==0)
        fprintf(1,'Processing %3d/%d files\n', i, num_images);
    end
    gt_file_name = [gt_path,'GT_IMG_',num2str(i),'.mat'];
    load(gt_file_name);
    input_img_name = strcat(path,'IMG_',num2str(i),'.jpg');
    im = imread(input_img_name);
    [h, w, c] = size(im);
    if (c == 3)
        im = rgb2gray(im);
    end     
    annPoints =  image_info{1}.location;
    gt_people_count = [ gt_people_count;length(annPoints)];
    [h, w, c] = size(im);
    %im_density = get_density_map_gaussian(im,annPoints);    
    %csvwrite([gt_path_csv ,'IMG_',num2str(i) '.csv'], im_density);       
end
disp(max(gt_people_count));