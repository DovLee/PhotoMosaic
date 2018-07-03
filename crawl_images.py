from icrawler.builtin import GoogleImageCrawler
from icrawler import ImageDownloader
from six.moves.urllib.parse import urlparse
import os

# http://icrawler.readthedocs.io/en/latest/builtin.html#search-engine-crawlers
# http://icrawler.readthedocs.io/en/latest/extend.html
# https://programtalk.com/vs2/python/5261/icrawler/icrawler/examples/google.py/
'''
should i get 200x200 image? - no
or
get randomly and crop it? - i've just resized the img

get only jpg file (no transparent image)
-> why it has to be like this?
---> because it's easier to process crawled imgs to the proper format, 400x400 3-channeled jpg file

'color', 'blackandwhite', 'transparent',
'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'

'''


class MyGoogleDownloader(ImageDownloader):  # override - saved gif as jpg and changed the name(i.e. 1.jpg)
    def get_filename(self, task, default_ext='jpg'):
        url_path = urlparse(task['file_url'])[2]
        if '.' in url_path:
            extension = url_path.split('.')[-1]
            if extension.lower() not in [
                'jpg', 'jpeg', 'png', 'bmp', 'tiff', 'ppm', 'pgm'
            ]:
                extension = default_ext
        else:
            extension = default_ext
        file_idx = self.fetched_num + self.file_idx_offset
        return '{}.{}'.format(file_idx, extension)


ROOT = 'TileImages'

filters = dict(
    size="medium",
    license='noncommercial'
)
colors = [
    'red', 'orange', 'yellow', 'green',
    'teal', 'blue', 'purple', 'pink',
    'white', 'gray', 'black', 'brown'
]
keywords = [
    'flower', 'food', 'painting',
    'cat', 'landscape', 'forest',
    'water', 'ocean', 'selfie'
]
num = 100  # total:10800 imgs
# total 10,800 images
for c_idx in range(len(colors)):
    google_crawler = GoogleImageCrawler(
        downloader_cls=MyGoogleDownloader,
        feeder_threads=1,
        parser_threads=1,
        downloader_threads=4,
        storage={'root_dir': os.path.join(ROOT, colors[c_idx])},
    )
    filters['color'] = colors[c_idx]
    for k_idx in range(len(keywords)):
        google_crawler.crawl(keyword=keywords[k_idx], filters=filters, offset=0, max_num=num,
                             min_size=(400, 400), max_size=None, file_idx_offset=k_idx*num)
