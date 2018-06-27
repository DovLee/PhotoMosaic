from scipy import misc
import numpy as np

def gcd(a, b):
    if a < b:
        (a, b) = (b, a)
    while b != 0:
        (a, b) = (b, a % b)
    return a

# os.walk a
img = misc.imread('sample.jpg')
#print img.mean(0).mean(0)

# 400x300->12 grids
# print img.shape # (h, w, 3)
len = 80 # mosaic size (len x len)
height, width = img.shape[0], img.shape[1]
# the best len is?
crust_h = height % len
crust_w = width % len
# fixed: h->w
count = 0
print range(0, height, len)
print range(0, width, len)

for y in range(0, height, len):# 0, 80, 160, 240//0, 60, 120, 180, 240
    for x in range(0, width, len):# 0, 80, 160, 240, 320//0, 60, 120, 180, 240
        img[y:y + len, x:x + len, :].mean(0).mean(0)
        count += 1
print count
#
#     if crust_w:
#         print img[y:y + len, width - crust_w:width, :].mean(0).mean(0)
#         count += 1
# if crust_h:
#     for x in range(0, width-len, len):
#         print img[height-crust_h:height, x:x+len, :].mean(0).mean(0)
#         count += 1
#     if crust_w:
#         print img[height-crust_h:height, width - crust_w:width, :].mean(0).mean(0)
#         count += 1
#     else:
#         print img[height-crust_h:height, width-len:width, :].mean(0).mean(0)
#         count += 1

# print count
# if len==80 then h==240:300 is not averaged (15+5 grids)
# if len==60 then w==360:400 is not averaged (30+5 grids)

