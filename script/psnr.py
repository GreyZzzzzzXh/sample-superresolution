import numpy as np
import math
from skimage import io as skio
from skimage import color as skco

im_gnd_path = '../images/Set5_gray/'
im_b_path = '../outputs/'
im_h_path = '../outputs/'

imname_gnd = ('baby_GT_gnd.bmp',
              'bird_GT_gnd.bmp',
              'butterfly_GT_gnd.bmp',
              'head_GT_gnd.bmp',
              'woman_GT_gnd.bmp')
imname_b = ('baby_GT_l_bicubic.bmp',
            'bird_GT_l_bicubic.bmp',
            'butterfly_GT_l_bicubic.bmp',
            'head_GT_l_bicubic.bmp',
            'woman_GT_l_bicubic.bmp')

num = len(imname_gnd)
border = (6, 6)

def shave(I, border):
    I = I[border[0]: -border[0], border[1]: -border[1]]
    return I

def psnr(im1, im2):
    imdff = im1 * 1.0 - im2 * 1.0
    mse = np.mean(imdff ** 2)
    return 10 * math.log10(255.0**2/mse)

def bicubic():
    psnr_b_sum = 0.

    for i in range(num):
        ''' load image '''
        im_b = skio.imread(im_b_path + imname_b[i]) # gray [0-255]
        im_gnd = skio.imread(im_gnd_path + imname_gnd[i])
        ''' remove border '''
        im_b = shave(im_b, border)
        im_gnd = shave(im_gnd, border)
        ''' PSNR '''
        psnr_b = psnr(im_gnd, im_b)
        psnr_b_sum = psnr_b_sum + psnr_b

    print('Mean PSNR for bicubic: {:.2f} dB'.format(psnr_b_sum / num))

def sr(model_name):
    psnr_h_sum = 0.
    imname_h = ('baby_GT_l_{}.bmp'.format(model_name),
                'bird_GT_l_{}.bmp'.format(model_name),
                'butterfly_GT_l_{}.bmp'.format(model_name),
                'head_GT_l_{}.bmp'.format(model_name),
                'woman_GT_l_{}.bmp'.format(model_name))

    for i in range(num):
        ''' load image '''
        im_h = skio.imread(im_h_path + imname_h[i])
        im_gnd = skio.imread(im_gnd_path + imname_gnd[i])
        ''' remove border '''
        im_h = shave(im_h, border)
        im_gnd = shave(im_gnd, border)
        ''' PSNR '''
        psnr_h = psnr(im_gnd, im_h)
        psnr_h_sum = psnr_h_sum + psnr_h

    print('Mean PSNR for {}: {:.2f} dB'.format(model_name, psnr_h_sum / num))

if __name__ == '__main__':
    bicubic()
    sr('srcnn')
    sr('fsrcnn')
    sr('espcn')
    sr('idn')
