clc; 
dataset = 'B';
dataset_name = ['shanghaitech_part_' dataset ];

test_data_path = ['../data/original/shanghaitech/part_' dataset '_final/test_data/images/'];
test_gt_path = ['../data/original/shanghaitech/part_' dataset '_final/test_data/ground-truth/'];

train_data_path = ['../data/original/shanghaitech/part_' dataset '_final/train_data/images/'];
train_gt_path = ['../data/original/shanghaitech/part_' dataset '_final/train_data/ground-truth/'];

if (dataset == 'A')
    num_images_test = 182;
else
    num_images_test = 316;
end

if (dataset == 'A')
    num_images_train = 300;
else
    num_images_train = 400;
end

gt_people_count = [];

% load test data
for i = 1:num_images_test  
    if (mod(i,10)==0)
        fprintf(1,'Processing %3d/%d files\n', i, num_images_test);
    end
    gt_file_name = [test_gt_path,'GT_IMG_',num2str(i),'.mat'];
    load(gt_file_name);
    input_img_name = strcat(test_data_path,'IMG_',num2str(i),'.jpg');
    %im = imread(input_img_name);   
    annPoints =  image_info{1}.location;
    gt_people_count = [ gt_people_count;length(annPoints)];        
end

% load trian data
for i = 1:num_images_train  
    if (mod(i,10)==0)
        fprintf(1,'Processing %3d/%d files\n', i, num_images_train);
    end
    gt_file_name = [train_gt_path,'GT_IMG_',num2str(i),'.mat'];
    load(gt_file_name);
    input_img_name = strcat(train_data_path,'IMG_',num2str(i),'.jpg');
    %im = imread(input_img_name);   
    annPoints =  image_info{1}.location;
    gt_people_count = [ gt_people_count;length(annPoints)];       
end

disp(min(gt_people_count));
disp(max(gt_people_count));
disp(sum(gt_people_count));
