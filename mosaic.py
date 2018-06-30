from scipy import misc
import json
import math
from PIL import Image

# http://www.compuphase.com/cmetric.htm
# http://python-colormath.readthedocs.io/en/latest/


def _color_difference(e1, e2):
    r_mean = 0.5 * (e1[0] + e2[0])
    diff = math.sqrt(sum((2 + r_mean, 4, 3 - r_mean) * (e1 - e2) ** 2))
    return diff


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

# print(color_difference(numpy.array([255, 255, 255]), numpy.array([0, 0, 0])))  # 765.0
'''
def gcd(a, b): # the best len is?
    if a < b:
        (a, b) = (b, a)
    while b != 0:
        (a, b) = (b, a % b)
    return a
'''
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
CELL_LENGTH = 10
root = 'TileImages/'
input_image = 'sample.jpg'


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
                'averageColor': (img[y:y + cell_len, x:x + cell_len, :].mean(0).mean(0)).tolist()
            }
            img_data[y][x] = cell_data

    # save image data as a file
    with open('target_data.txt', 'w') as out_file:
        json.dump(img_data, out_file)


'''
read target_data.txt
start making the result. the image.
    for each cell,
        choose the right tile (by Riemersma metric)
        paste it
save the result in png format
'''
'''
def color_distance(e1, e2):
    r_mean = (e1[0] + e2[0]) / 2
    r = e1[0] - e2[0]
    g = e1[1] - e2[1]
    b = e1[2] - e2[2]
    return math.sqrt((((512 + r_mean) * r * r) >> 8) + 4 * g * g + (((767 - r_mean) * b * b) >> 8))
'''


def do_mosaic():
    with open('target_data.txt', 'r') as target_file:
        img_data = json.load(target_file)
    with open('tile_data.txt', 'r') as tile_file:
        tile_data = json.load(tile_file)

    # height, width = 300, 400
    input_img = Image.open(input_image)
    for col, rows in img_data.items():
        for row, values in rows.items():
            tile_num = 0
            min_diff = 800.0
            for idx in tile_data:
                # print(idx + '.jpg')
                diff = color_difference(values['averageColor'], tile_data[idx])
                if diff < min_diff:
                    tile_num = idx
                    min_diff = diff
            tile_length = values['length']
            '''
            tile = misc.imread('TileImages/{}.jpg'.format(tile_num))
            tile = misc.imresize(tile, (tile_length, tile_length))
            '''
            tile = Image.open(root + tile_num + '.jpg')
            tile = tile.resize((tile_length, tile_length))
            # now i have to paste this tile.... but how?
            input_img.paste(tile, (int(row), int(col)))  # row, col?
            print('pasted')
    input_img.save('output2.jpg', 'JPEG')

photo_process(input_image)
do_mosaic()
'''
tile = Image.open(root + '1' + '.jpg')
tile = tile.resize((80, 80))
sample = Image.open('test_sample.jpg')
sample.paste(tile, (0, 0))
sample.save('test_sample.jpg', 'JPEG')
'''