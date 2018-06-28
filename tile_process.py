import os
from scipy import misc
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


def tile_image_process():
    tile_img_data = {}
    for root, dirs, files in os.walk('TileImages', topdown=False):
        for name in files:
            img = misc.imread(os.path.join(root, name))
            img = misc.imresize(img, (400, 400))
            misc.imsave(os.path.join(root, name), img)  # resize and save the tile
            tile_img_data[name.split('.')[0]] = (img[:, :, :].mean(0).mean(0)).tolist()  # calculate average color

    with open('tile__data.txt', 'w') as out_file:  # save the data
        json.dump(tile_img_data, out_file)


tile_image_process()