from scipy import misc
import numpy as np
import json

def gcd(a, b): # the best len is?
    if a < b:
        (a, b) = (b, a)
    while b != 0:
        (a, b) = (b, a % b)
    return a
# find a number of tile images
# tiles should be named as a number.(1, 2, 3, ...)
# for each tile, calculate average color
# make a dictionary( {1: [122, 234, 56], 2:[.., .., ..], ... } )
# save it using json
def TileImageProcess():
    tile_img_data = {}
    for
    img = misc.imread('1.jpg')
    img[:, :, :].mean(0).mean(0)
# os.walk a
img = misc.imread('sample.jpg')

# 400x300->12 grids
# print img.shape # (h, w, 3)
len = 80 # mosaic size (len x len)
height, width = img.shape[0], img.shape[1]
img_data = {} # { #h1:{ #w1:{'length':80, 'averageColor':[100, 125, 50] }, #w2:{}, ...} #h2:{},... }
'''
img[240:320, 0:80,:].mean(0).mean(0) == img[240:300, 0:80,:].mean(0).mean(0) given 400x300 image
But afterwards, crust has to be considered(maybe at the point the final image is processed. crop it)
'''
# for each cell, calculate average color
for y in range(0, height, len):
    img_data[y] = {}
    for x in range(0, width, len):
        cell_data = {
            'length': len,
            'averageColor': (img[y:y + len, x:x + len, :].mean(0).mean(0)).tolist()
        }
        img_data[y][x] = cell_data

# save image data as a file
with open('image_data.txt', 'w') as out_file:
    json.dump(img_data, out_file)
'''
# Why I decided use JSON?
(https://docs.python.org/3.4/tutorial/inputoutput.html)
(https://docs.python.org/3.4/library/json.html#module-json)
read() only returns strings, which will have to be passed to a function like int()
(takes a string like '123' and returns its numeric value 123)
When you want to save more complex data types like nested lists and dictionaries, parsing and serializing by hand becomes complicated.
Rather than doing this, I'll to use the popular data interchange format called JSON (JavaScript Object Notation)
The standard module called json can take Python data hierarchies, and convert them to string representations(aka serializing).
Reconstructing the data from the string representation is called deserializing.
Between serializing and deserializing, the string representing the object may have been stored in a file or data,
or sent over a network connection to some distant machine.
json.dump(x, f)
'''

