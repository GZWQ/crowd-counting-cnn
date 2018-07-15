clc; 
seed = 95461354;
rng(seed)
N = 9;
dataset_name = ['ucsd_patches_' num2str(N)];

image_path = ['../data/original/uscd/train_data/images/'];
out_gt_path_csv = ['../data/original/uscd/train_data/gt_truth_csv/'];
gt_path = ['../data/original/uscd/train_data/ground_truth/'];

output_path = '../data/ucsd_formatted_trainval/';
train_path_img = strcat(output_path, dataset_name,'/train/');
train_path_den = strcat(output_path, dataset_name,'/train_den/');
val_path_img = strcat(output_path, dataset_name,'/val/');
val_path_den = strcat(output_path, dataset_name,'/val_den/');


mkdir(output_path)
mkdir(train_path_img);
mkdir(train_path_den);
mkdir(val_path_img);
mkdir(val_path_den);


num_images = 800;

num_val = ceil(num_images*0.1);
indices = randperm(num_images);

load([gt_path,'vidf1_33_roi_mainwalkway.mat']);

for idx = 1:num_images
    i = indices(idx);
    if (mod(idx,10)==0)
        fprintf(1,'Processing %3d/%d files\n', idx, num_images);
    end
    pic_num = floor((i-1)/200)+3;
    t = mod(i,200);
    if (t==0)
        t=200;
    end
    gt_file_name = [gt_path,'vidf1_33_00',num2str(pic_num),'_frame_full.mat'];
    load(gt_file_name);
    input_img_name = strcat(image_path,'IMG_',num2str(i),'.jpg');
    im = imread(input_img_name);
    [h, w, c] = size(im);
    if (c == 3)
        im = rgb2gray(im);
    end
    
    wn2 = w/8; hn2 = h/8;
    wn2 =8 * floor(wn2/8);
    hn2 =8 * floor(hn2/8);
    
    annPoints =  frame{t}.loc;
    if( w <= 2*wn2 )
        im = imresize(im,[ h,2*wn2+1]);
        annPoints(:,1) = annPoints(:,1)*2*wn2/w;
    end
    if( h <= 2*hn2)
        im = imresize(im,[2*hn2+1,w]);
        annPoints(:,2) = annPoints(:,2)*2*hn2/h;
    end
    [h, w, c] = size(im);
    a_w = wn2+1; b_w = w - wn2;
    a_h = hn2+1; b_h = h - hn2;
    
    im_density = get_density_map_gaussian_ucsd(im,annPoints);
    for j = 1:N
        
        x = floor((b_w - a_w) * rand + a_w);
        y = floor((b_h - a_h) * rand + a_h);
        x1 = x - wn2; y1 = y - hn2;
        x2 = x + wn2-1; y2 = y + hn2-1;
        
        
        im_sampled = im(y1:y2, x1:x2,:);
        im_density_sampled = im_density(y1:y2,x1:x2);
        
        annPoints_sampled = annPoints(annPoints(:,1)>x1 & ...
            annPoints(:,1) < x2 & ...
            annPoints(:,2) > y1 & ...
            annPoints(:,2) < y2,:);
        annPoints_sampled(:,1) = annPoints_sampled(:,1) - x1;
        annPoints_sampled(:,2) = annPoints_sampled(:,2) - y1;
        img_idx = strcat(num2str(i), '_',num2str(j));        

        if(idx < num_val)
            imwrite(im_sampled, [val_path_img num2str(img_idx) '.jpg']);
            csvwrite([val_path_den num2str(img_idx) '.csv'], im_density_sampled);
        else
            imwrite(im_sampled, [train_path_img num2str(img_idx) '.jpg']);
            csvwrite([train_path_den num2str(img_idx) '.csv'], im_density_sampled);
        end
        
    end
    
end

