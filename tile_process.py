import os
from scipy import misc
import numpy
from PIL import Image
import json
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


size = (400, 400)


def tile_image_process2():
    tile_img_data = {}
    for root, dirs, files in os.walk('TileImages', topdown=False):
        for file in files:
            print(file)
            name, ext = os.path.splitext(file)
            im = Image.open(os.path.join(root, file))
            im = im.resize(size)
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
    tile_img_data = {}
    for root, dirs, files in os.walk('TileImages', topdown=True):
        for _dir in dirs:
            tile_img_data[_dir] = {}
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
            tile_img_data[d][name] = (img[:, :, :].mean(0).mean(0)).tolist()  # calculate average color
    dir_data = {}
    for k, v in tile_img_data.items():
        with open('TileImages/{}/tile_data.txt'.format(k), 'w') as out_file:  # save the data
            json.dump(v, out_file)
        dir_rgb = []
        for color in v.values():
            dir_rgb.append(color)
        #print(dir_rgb)
        dir_color = numpy.asarray(dir_rgb)
        dir_mean = numpy.mean(dir_color, axis=0)
        #print(dir_mean)
        dir_data[k] = dir_mean.tolist()
    with open('directory_data.txt', 'w') as out_file:  # save the data
        json.dump(dir_data, out_file)


tile_image_process()

'''
from PIL import Image
import glob, os
infile = '1.jpg'
size = (400, 400)
file, ext = os.path.splitext(infile)
im = Image.open(infile)
im = im.resize(size)
im.save(file + ".png", "PNG")
'''
'''

root = 'TileImages'
name = '1061.jpg'
img = misc.imread(os.path.join(root, name), 'RGBA')
print(img.ndim)
print(img.shape)
# print('{}: {}'.format(name, img.shape))
# img = misc.imresize(img, (400, 400))
# print('resized {}: {}'.format(name, img.shape))
# misc.imsave(os.path.join(root, name), img)  # resize and save the tile
# print(img[:, :, :].mean(0).mean(0))  # calculate average color
'''
