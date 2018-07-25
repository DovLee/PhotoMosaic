from scipy import misc, ndimage
import json
import math
from PIL import Image
import color_transfer
import time
import os
import random
import numpy as np
from skimage import color
# http://www.compuphase.com/cmetric.htm
# http://python-colormath.readthedocs.io/en/latest/
# https://stackoverflow.com/questions/6094957/high-pass-filter-for-image-processing-in-python-by-using-scipy-numpy
# https://www.safaribooksonline.com/library/view/programming-computer-vision/9781449341916/ch01.html
# https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python


def color_difference(e1, e2):
    r_mean = (e1[0] + e2[0]) / 2
    r = e1[0] - e2[0]
    g = e1[1] - e2[1]
    b = e1[2] - e2[2]
    tmp = (512 + r_mean) * r * r
    x = round(tmp) >> 8
    y = 4 * g * g
    z = round((767 - r_mean) * b * b) >> 8
    diff = math.sqrt(x + y + z)
    return diff


CELL_LENGTH = 20
ROOT = 'TileImages'
#input_image = 'sample.jpg'
#input_image = 'butterfly_large.jpg'
input_image = 'life_and_death.jpg'
#input_image = 'lion.jpg'
#input_image = 'game-of-thrones-4000x2231.jpg'
#input_image = 'Large_Scaled_Forest_Lizard.jpg'
LEN_KEYWORDS = 9
TILE_MAX_NUM = 100
# DIR_MAX_NUM = TILE_MAX_NUM * LEN_KEYWORDS
DIR_MAX_NUM = 100
INTERVAL = 64
d_list = list(range(0, 257, INTERVAL))

'''
def to_rgb(im):
    w, h = im.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 0] = im
    ret[:, :, 1] = ret[:, :, 2] = ret[:, :, 0]
    return ret


def rgb2lab(input_color):
    num = 0
    RGB = [0, 0, 0]

    for value in input_color:
        value = float(value) / 255

        if value > 0.04045:
            value = ((value + 0.055) / 1.055) ** 2.4
        else:
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0, ]

    X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
    Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
    Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
    XYZ[0] = round(X, 4)
    XYZ[1] = round(Y, 4)
    XYZ[2] = round(Z, 4)

    XYZ[0] = float(XYZ[0]) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
    XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ:

        if value > 0.008856:
            value = value ** (1/3)
        else:
            value = (7.787 * value) + (16 / 116)

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = (116 * XYZ[1]) - 16
    a = 500 * (XYZ[0] - XYZ[1])
    b = 200 * (XYZ[1] - XYZ[2])

    Lab[0] = round(L, 4)
    Lab[1] = round(a, 4)
    Lab[2] = round(b, 4)

    return Lab


def to_lab(img):
    im = np.asarray(img).copy()
    width, height = img.size
    for w in range(width):
        for h in range(height):
            num = 0
            RGB = [0, 0, 0]
            for value in im[h][w]:
                value = float(value) / 255

                if value > 0.04045:
                    value = ((value + 0.055) / 1.055) ** 2.4
                else:
                    value = value / 12.92

                RGB[num] = value * 100
                num = num + 1

            XYZ = [0, 0, 0, ]

            X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
            Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
            Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
            XYZ[0] = round(X, 4)
            XYZ[1] = round(Y, 4)
            XYZ[2] = round(Z, 4)

            XYZ[0] = float(XYZ[0]) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
            XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
            XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

            num = 0
            for value in XYZ:

                if value > 0.008856:
                    value = value ** (1/3)
                else:
                    value = (7.787 * value) + (16 / 116)

                XYZ[num] = value
                num = num + 1

            Lab = [0, 0, 0]

            L = (116 * XYZ[1]) - 16
            a = 500 * (XYZ[0] - XYZ[1])
            b = 200 * (XYZ[1] - XYZ[2])

            Lab[0] = round(L, 4)
            Lab[1] = round(a, 4)
            Lab[2] = round(b, 4)

            im[h][w] = Lab
    return Image.fromarray(im, 'LAB')
'''


def photo_process(file_name):
    img = misc.imread(file_name)
    cell_len = CELL_LENGTH  # mosaic size (len x len)
    height, width = img.shape[0], img.shape[1]
    img_data = {}  # { #h1:{ #w1:{'length':80, 'averageColor':[100, 125, 50] }, #w2:{}, ...} #h2:{},... }
    '''
    img[240:320, 0:80,:].mean(0).mean(0) == img[240:300, 0:80,:].mean(0).mean(0) given 400x300 image
    But afterwards, crust has to be considered(maybe at the point the final image is processed. crop it)
    '''
    # for each cell, calculate average color
    for y in range(0, height, cell_len):
        img_data[y] = {}
        for x in range(0, width, cell_len):
            cell_data = {
                'length': cell_len,
                'averageColor': [round(e) for e in (img[y:y + cell_len, x:x + cell_len, :].mean(0).mean(0)).tolist()]
            }
            img_data[y][x] = cell_data
    return img_data


def mosaic(img_data):  # seems less repetition code is not working..
    with open('directory_data.txt', 'r') as dir_file:
        dir_data = json.load(dir_file)
    input_img = Image.open(input_image)
    is_used = {}
    for d in dir_data:
        is_used[d] = [False] * (DIR_MAX_NUM + 1)
    with open('tile_data.txt', 'r') as tile_file:
        tile_data = json.load(tile_file)
    for col, rows in img_data.items():
        for row, values in rows.items():
            dir_distance = {}
            for d in dir_data:
                dir_distance[d] = color_difference(values['averageColor'], dir_data[d])
            sorted_by_value = sorted(dir_distance.items(), key=lambda kv: kv[1])
            nearest_dir = [sorted_by_value[0][0], sorted_by_value[1][0]]
            tile_length = values['length']
            dir_name = ''
            tile_num = 0
            m_diff = 800.0
            min_dir = ''
            min_idx = ''
            min_diff = 800.0
            for d in nearest_dir:
                for idx in tile_data[d]:
                    diff = color_difference(values['averageColor'], tile_data[d][idx])
                    if diff < min_diff:
                        flag = is_used[d][int(idx)]
                        if flag is True:
                            min_dir = d
                            min_idx = idx
                            m_diff = diff
                            continue
                        dir_name = d
                        tile_num = idx
                        min_diff = diff
            if min_diff > 40 and m_diff < min_diff:
                src = misc.imread(os.path.join(ROOT, min_dir, str(min_idx) + '.jpg'))
                #src = numpy.asarray(Image.new('RGB', (tile_length, tile_length), tuple(values['averageColor'])))
                dst = misc.imread(os.path.join(ROOT, dir_name, str(tile_num) + '.jpg'))
                new = color_transfer.color_transfer(src, dst)
                tile = Image.fromarray(new)
                tile = tile.resize((tile_length, tile_length))
                input_img.paste(tile, (int(row), int(col)))
                is_used[min_dir] = [False] * (DIR_MAX_NUM + 1)
                continue
            tile = Image.open(os.path.join(ROOT, dir_name, str(tile_num) + '.jpg'))
            tile = tile.resize((tile_length, tile_length))
            input_img.paste(tile, (int(row), int(col)))
            is_used[dir_name][int(tile_num)] = True
    input_img.save(input_image.split('.')[0] + '_mosaic_{}px.jpg'.format(str(tile_length)), 'JPEG')


def fast_mosaic(file_name):
    im = Image.open(file_name)
    data = np.array(im, dtype=float)
    #random_mosaic = np.array(create_random_mosaic(im), dtype=float)
    random_mosaic = misc.imread(os.path.join('Test_fast_mode', 'random_mosaic.jpg'))
    # random_mosaic_low_pass = ndimage.gaussian_filter(random_mosaic, 1)
    # Another way of making a highpass filter is to simply subtract a lowpass
    # filtered image from the original. Here, we'll use a simple gaussian filter
    # to "blur" (i.e. a lowpass filter) the original.
    low_pass = ndimage.gaussian_filter(data, 3)
    #high_pass = data - ndimage.gaussian_filter(data, 6)
    high_pass = data - low_pass

    weighted = 0.2*random_mosaic + 0.6*low_pass + 0.8*high_pass
    misc.imsave(os.path.join('Test_fast_mode', 'result_268.jpg'), weighted)


def create_random_mosaic(im):
    cell_len = CELL_LENGTH  # mosaic size (len x len)
    height, width = im.size
    li = [f for f in os.listdir(ROOT) if os.path.isdir(os.path.join(ROOT, f))]
    for y in range(0, height, cell_len):
        for x in range(0, width, cell_len):
            random_dir = li[random.randint(0, len(li)) - 2]
            random_dir = os.path.join(ROOT, random_dir)
            random_file = random.choice([
                x for x in os.listdir(random_dir)
                if os.path.isfile(os.path.join(random_dir, x))
            ])
            tile = Image.open(os.path.join(random_dir, random_file))

            tile = tile.resize((cell_len, cell_len))
            im.paste(tile, (int(y), int(x)))
    return im

# RGB weighted sum
def decent_mosaic(img_data):
    with open('directory_data.txt', 'r') as dir_file:
        dir_data = json.load(dir_file)
    input_img = Image.open(input_image)
    data = np.array(input_img, dtype=float)
    low_pass = ndimage.gaussian_filter(data, 3)
    high_pass = data - low_pass
    is_used = {}
    for d in dir_data:
        is_used[d] = [False] * (DIR_MAX_NUM + 1)
    with open('tile_data.txt', 'r') as tile_file:
        tile_data = json.load(tile_file)
    for col, rows in img_data.items():
        for row, values in rows.items():
            dir_distance = {}
            for d in dir_data:
                dir_distance[d] = color_difference(values['averageColor'], dir_data[d])
            sorted_by_value = sorted(dir_distance.items(), key=lambda kv: kv[1])
            nearest_dir = [sorted_by_value[0][0], sorted_by_value[1][0]]
            tile_length = values['length']
            dir_name = ''
            tile_num = 0
            m_diff = 800.0
            min_dir = ''
            min_idx = ''
            min_diff = 800.0
            for d in nearest_dir:
                for idx in tile_data[d]:
                    diff = color_difference(values['averageColor'], tile_data[d][idx])
                    if diff < min_diff:
                        flag = is_used[d][int(idx)]
                        if flag is True:
                            min_dir = d
                            min_idx = idx
                            m_diff = diff
                            continue
                        dir_name = d
                        tile_num = idx
                        min_diff = diff
            if min_diff > 40 and m_diff < min_diff:
                src = misc.imread(os.path.join(ROOT, min_dir, str(min_idx) + '.jpg'))
                #src = numpy.asarray(Image.new('RGB', (tile_length, tile_length), tuple(values['averageColor'])))
                dst = misc.imread(os.path.join(ROOT, dir_name, str(tile_num) + '.jpg'))
                new = color_transfer.color_transfer(src, dst)
                tile = Image.fromarray(new)
                tile = tile.resize((tile_length, tile_length))
                input_img.paste(tile, (int(row), int(col)))
                is_used[min_dir] = [False] * (DIR_MAX_NUM + 1)
                continue
            tile = Image.open(os.path.join(ROOT, dir_name, str(tile_num) + '.jpg'))
            tile = tile.resize((tile_length, tile_length))
            input_img.paste(tile, (int(row), int(col)))
            is_used[dir_name][int(tile_num)] = True
    result_image_data = 0.4*np.array(input_img, dtype=float) + 0.7*low_pass + 0.8*high_pass
    misc.imsave(input_image.split('.')[0] + '_decent_mosaic_g3_82_{}px.jpg'.format(str(tile_length)), result_image_data)

# LAB weighted sum (supposed to be the standard, though the result is unsatisfiable)
def decent_mosaic2(img_data):
    with open('directory_data.txt', 'r') as dir_file:
        dir_data = json.load(dir_file)
    input_img = Image.open(input_image)
    data = np.array(input_img.convert('L'), dtype=float)
    low_pass = ndimage.gaussian_filter(data, 3)
    high_pass = data - low_pass
    max_value = np.amax(high_pass)
    min_value = np.amin(high_pass)
    high_pass = 100 * (high_pass - min_value) / (max_value - min_value)  # scaling [0, 100]
    is_used = {}
    for d in dir_data:
        is_used[d] = [False] * (DIR_MAX_NUM + 1)
    with open('tile_data.txt', 'r') as tile_file:
        tile_data = json.load(tile_file)
    for col, rows in img_data.items():
        for row, values in rows.items():
            dir_distance = {}
            for d in dir_data:
                dir_distance[d] = color_difference(values['averageColor'], dir_data[d])
            sorted_by_value = sorted(dir_distance.items(), key=lambda kv: kv[1])
            nearest_dir = [sorted_by_value[0][0], sorted_by_value[1][0]]
            tile_length = values['length']
            dir_name = ''
            tile_num = 0
            m_diff = 800.0
            min_dir = ''
            min_idx = ''
            min_diff = 800.0
            for d in nearest_dir:
                for idx in tile_data[d]:
                    diff = color_difference(values['averageColor'], tile_data[d][idx])
                    if diff < min_diff:
                        flag = is_used[d][int(idx)]
                        if flag is True:
                            min_dir = d
                            min_idx = idx
                            m_diff = diff
                            continue
                        dir_name = d
                        tile_num = idx
                        min_diff = diff
            if min_diff > 40 and m_diff < min_diff:
                src = misc.imread(os.path.join(ROOT, min_dir, str(min_idx) + '.jpg'))
                #src = numpy.asarray(Image.new('RGB', (tile_length, tile_length), tuple(values['averageColor'])))
                dst = misc.imread(os.path.join(ROOT, dir_name, str(tile_num) + '.jpg'))
                new = color_transfer.color_transfer(src, dst)
                tile = Image.fromarray(new)
                tile = tile.resize((tile_length, tile_length))
                input_img.paste(tile, (int(row), int(col)))
                is_used[min_dir] = [False] * (DIR_MAX_NUM + 1)
                continue
            tile = Image.open(os.path.join(ROOT, dir_name, str(tile_num) + '.jpg'))
            tile = tile.resize((tile_length, tile_length))
            input_img.paste(tile, (int(row), int(col)))
            is_used[dir_name][int(tile_num)] = True

    #result_image_data = 0.4*np.array(input_img, dtype=float) + 0.7*low_pass + 0.8*high_pass
    input_img_data = np.asarray(input_img)/255  # scaling [0, 1]
    input_img_data = color.rgb2lab(input_img_data)
    l, a, b = np.split(input_img_data, 3, axis=2)
    height, width = high_pass.shape
    result_l = 0.3*l + 0.7*high_pass.reshape(height, width, 1)
    tmp = np.concatenate((result_l, a, b), axis=2)
    result_image_data = color.lab2rgb(tmp)*255
    misc.imsave(input_image.split('.')[0] + '_decent_mosaic_lab_g3_3_7_{}px.jpg'.format(str(tile_length)), result_image_data)
    #tmp.save(input_image.split('.')[0] + '_decent_mosaic_lab_g3_11_{}px.jpg'.format(str(tile_length)), 'JPEG')


'''
im = Image.open(input_image)
data = np.array(im, dtype=float)
low_pass = ndimage.gaussian_filter(data, 10)
high_pass = data - low_pass
misc.imsave(os.path.join('Test_fast_mode', 'high_pass_gamma10.jpg'), high_pass)
'''
#fast_mosaic(input_image)
#mosaic(photo_process(input_image))
decent_mosaic2(photo_process(input_image))
