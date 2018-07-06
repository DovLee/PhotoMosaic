import os
import numpy
from PIL import Image
import json
import time
import shutil

# https://www.tutorialspoint.com/python/os_walk.htm


# find a number of tile images
# tiles should be named as a number.(1, 2, 3, ...)
# for each tile, calculate average color
# make a dictionary( {1: [122, 234, 56], 2:[.., .., ..], ... } )
# save it using json
'''
"blackandwhite”, “transparent”, “red”, “orange”, “yellow”, “green”, “teal”, “blue”, “purple”, “pink”, “white”, “gray”, “black”, “brown”
-> save at different directories? i dont think so
# https://www.w3schools.com/colors/colors_groups.asp
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
teal = (0, 128, 128)
blue = (0, 0, 255)
purple = (128, 0, 128)
pink = (255, 192, 203)
white = (255, 255, 255)
gray = (128, 128, 128)
black = (0, 0, 0)
brown = (165, 42, 42)

'''
INTERVAL = 64
d_list = list(range(0, 257, INTERVAL))
size = (400, 400)
ROOT = 'TileImages'
SPLIT_SIZE = 100


def tile_image_process2():
    tile_img_data = {}
    for root, dirs, files in os.walk('TileImages', topdown=False):
        for file in files:
            print(file)
            name, ext = os.path.splitext(file)
            im = Image.open(os.path.join(root, file))
            im = im.resize(size)
            print(im.mode)
            if im.mode is not 'RGB':
                im = im.convert('RGB')
                print('{}: {} mode had converted'.format(file, im.mode))
            im.save(os.path.join(root, name) + '.jpg', 'JPEG')  # resize and save the tile
            img = numpy.asarray(im)
            tile_img_data[name] = (img[:, :, :].mean(0).mean(0)).tolist()  # calculate average color
            '''
            img = misc.imread(os.path.join(root, name))
            print('{}: {}'.format(name, img.shape))
            img = misc.imresize(img, (400, 400))
            print('resized {}: {}'.format(name, img.shape))
            if img.mode == 'P':
                img = img.convert('RGBA')
            misc.imsave(os.path.join(root, name), img)  # resize and save the tile
            tile_img_data[name.split('.')[0]] = (img[:, :, :].mean(0).mean(0)).tolist()  # calculate average color
            '''
    with open('tile_data.txt', 'w') as out_file:  # save the data
        json.dump(tile_img_data, out_file)


def tile_image_process():
    tmp_tile_data = {}
    for root, dirs, files in os.walk(ROOT, topdown=True):
        for d in dirs:
            tmp_tile_data[d] = {}
        for file in files:
            d = os.path.split(root)[-1]
            name, ext = os.path.splitext(file)
            im = Image.open(os.path.join(root, file))
            im = im.resize(size)
            if im.mode is not 'RGB':
                im = im.convert('RGB')
            os.remove(os.path.join(root, file))
            im.save(os.path.join(root, name) + '.jpg', 'JPEG')  # resize and save the tile
            img = numpy.asarray(im)
            tmp_tile_data[d][name] = [round(e)
                                      for e in (img[:, :, :].mean(0).mean(0)).tolist()]  # calculate average color
    tile_data = {}
    for root, dirs, files in os.walk(ROOT, topdown=True):
        for d in dirs:
            idx = 0
            for tile, rgb in sorted(tmp_tile_data[d].items(), key=lambda e: (e[1][0], e[1][1], e[1][2])):
                dir_num = int(idx / SPLIT_SIZE)
                name = str(idx % SPLIT_SIZE + 1)
                new_dir = '{}_{}'.format(d, dir_num)
                if not os.path.exists(os.path.join(ROOT, new_dir)):
                    os.makedirs(os.path.join(ROOT, new_dir))
                    tile_data[new_dir] = {}
                shutil.move(os.path.join(ROOT, d, tile + '.jpg'),
                            os.path.join(ROOT, new_dir, name + '.jpg'))
                tile_data[new_dir][name] = rgb
                idx += 1
            os.rmdir(os.path.join(ROOT, d))
    dir_data = {}
    with open(os.path.join('tile_data.txt'), 'w') as out_file:  # save the data
        json.dump(tile_data, out_file)
    for d, tiles in tile_data.items():
        dir_rgb = []
        for color in tiles.values():
            dir_rgb.append(color)
        dir_color = numpy.asarray(dir_rgb)
        dir_mean = numpy.mean(dir_color, axis=0)
        dir_data[d] = [round(e) for e in dir_mean.tolist()]
    with open('directory_data.txt', 'w') as out_file:  # save the data
        json.dump(dir_data, out_file)


def tile_image_process_per_rgb_value():
    tile_img_data = {}
    for root, dirs, files in os.walk('TileImages', topdown=True):
        file_idx = {}
        for dR in d_list[1:]:
            for dG in d_list[1:]:
                for dB in d_list[1:]:
                    d = '{}.{}.{}'.format(dR, dG, dB)
                    if not os.path.exists(os.path.join(root, '{}.{}.{}'.format(dR, dG, dB))):
                        os.makedirs(os.path.join(root, '{}.{}.{}'.format(dR, dG, dB)))
                    tile_img_data[d] = {}
                    file_idx[d] = 1
        for file in files:
            name, ext = os.path.splitext(file)
            im = Image.open(os.path.join(root, file))
            im = im.resize(size)
            if im.mode is not 'RGB':
                im = im.convert('RGB')
            img = numpy.asarray(im)
            color = [round(e) for e in (img[:, :, :].mean(0).mean(0)).tolist()]
            d = []
            for c in color:
                for idx in range(len(d_list)-1):
                    if c in range(d_list[idx], d_list[idx+1]):
                        d.append(d_list[idx+1])
            directory = '{}.{}.{}'.format(d[0], d[1], d[2])
            im.save(os.path.join(root, directory, str(file_idx[directory])) + '.jpg', 'JPEG')  # save the tile
            os.remove(os.path.join(root, file))
            tile_img_data[directory][file_idx[directory]] = color
            file_idx[directory] += 1
        break
    for k, v in tile_img_data.items():
        with open(os.path.join(root, k, 'tile_data.txt'), 'w') as out_file:  # save the data
            json.dump(v, out_file)


start_time = time.time()
tile_image_process()
elapsed_time = time.time() - start_time
print(elapsed_time)

