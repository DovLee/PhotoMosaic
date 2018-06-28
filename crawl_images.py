from icrawler.builtin import GoogleImageCrawler
from icrawler import Downloader, ImageDownloader
from six.moves.urllib.parse import urlparse

# http://icrawler.readthedocs.io/en/latest/builtin.html#search-engine-crawlers
# http://icrawler.readthedocs.io/en/latest/extend.html
# https://programtalk.com/vs2/python/5261/icrawler/icrawler/examples/google.py/
'''
should i get 200x200 image?
or
get randomly and crop it?

get only jpg file (no transparent image)
-> why it has to be like this?

'color', 'blackandwhite', 'transparent', 'red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple', 'pink', 'white', 'gray', 'black', 'brown'

'''


class MyGoogleDownloader(ImageDownloader):  # override
    def get_filename(self, task, default_ext='png'):
        extension = 'png'  # always save image in png format
        file_idx = self.fetched_num + self.file_idx_offset
        return '{}.{}'.format(file_idx, extension)


google_crawler = GoogleImageCrawler(
    downloader_cls=MyGoogleDownloader,
    feeder_threads=1,
    parser_threads=1,
    downloader_threads=4,
    storage={'root_dir': 'TileImages'},
)
filters = dict(
    size="medium",
    color='color',
    license='noncommercial'
)
colors = [
    'red', 'orange', 'yellow', 'green',
    'teal', 'blue', 'purple', 'pink',
    'white', 'gray', 'black', 'brown']
num = 10
for idx in range(len(colors)):
    filters['color'] = colors[idx]
    google_crawler.crawl(keyword='forest', filters=filters, offset=0, max_num=num,
                         min_size=(200, 200), max_size=None, file_idx_offset=idx*num)
