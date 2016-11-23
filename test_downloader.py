import os
from webpagedownloader import WebPageDownloader

url = "http://imdb.com"
data_dir = os.getcwd() + '/sample'
print(data_dir)
wpd = WebPageDownloader(url, data_dir)
wpd.save_all_assets()
