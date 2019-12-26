% =========================================================================
% Convert Set5 dataset to gray format and downsample
% =========================================================================
close all;
clear all;

%% set parameters
testfolder = '../images/Set5/';
targetfolder = '../images/Set5_gray/';
up_scale = 3;
filepaths = dir(fullfile(testfolder,'*.bmp'));

for i = 1 : length(filepaths)
   
    %% read ground truth image
    [add,imname,type] = fileparts(filepaths(i).name);
    im = imread([testfolder imname type]);

    %% work on illuminance only
    if size(im,3) > 1
        im_ycbcr = rgb2ycbcr(im);
        im = im_ycbcr(:, :, 1);
    end

    % due to dvpp limits, height and width should also be even 
    im_gnd = modcrop(im, up_scale * 2);
    im_gnd = single(im_gnd)/255;

    % downsampling    
    im_l = imresize(im_gnd, 1/up_scale, 'bicubic');
    
    %% save 
    imwrite(im_gnd, [targetfolder imname '_gnd.bmp']);
    imwrite(im_l, [targetfolder imname '_l.bmp']);
end