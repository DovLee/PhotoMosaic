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

'''


size = (400, 400)


def tile_image_process():
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
